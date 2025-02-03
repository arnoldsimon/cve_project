import requests
from tqdm import tqdm
from datetime import datetime, timedelta

from config import CONFIG
import preprocess_helper as pp
import database_helper as db

BASE_URL : str 			= CONFIG["fetch_url"]
RESULTS_PER_PAGE : int 	= CONFIG["results_per_page"] 
SYNC_INTERVAL : int		= CONFIG["sync_interval"]

#fetch -> preprocess -> store
def fetch_changes(change_start: datetime, change_end: datetime):

	start_indx: int = 0
	while True:
		try:
			params = {
				'lastModStartDate'	: change_start,
				'lastModEndDate'	: change_end,
				'startIndex' 		: start_indx,
				'resultsPerPage' 	: RESULTS_PER_PAGE
			}
			response = requests.get(BASE_URL, params = params, timeout = 10)
			response.raise_for_status()
			if response.headers.get("Content-Type") != "application/json":
				raise Exception("The returned response did not contain json data.")

			res_json = response.json()
			
			if "vulnerabilities" not in res_json:
				raise Exception("Vulnerabilities field missing from the response json.") 
			if len(res_json["vulnerabilities"]) == 0:
				break

			cve_list = res_json["vulnerabilities"]
				
			#preprocess and store updated info
			for cve_info in tqdm(cve_list, desc = "Fetching modifications"):
				
				if pp.is_cve_invalid(cve_info):
					#log invalid cve data
					continue
				else:
					#store valid cve update
					db.update_cve(cve_info["cve"]["id"], cve_info["cve"])

			start_indx = start_indx + RESULTS_PER_PAGE

		except Exception as e:
			print("Error: {}".format(e))


def fetch_new(pub_start: datetime, pub_end: datetime):

	start_indx : int = 0
	unique_cve_ids : list = []
	while True:
		try:
			params = {
				'pubStartDate'	: pub_start,
				'pubEndDate'	: pub_end,
				'startIndex' 		: start_indx,
				'resultsPerPage' 	: RESULTS_PER_PAGE
			}
			response = requests.get(BASE_URL, params = params, timeout = 10)
			response.raise_for_status()
			if response.headers.get("Content-Type") != "application/json":
				raise Exception("The returned response did not contain json data.")

			res_json = response.json()
			
			if "vulnerabilities" not in res_json:
				raise Exception("Vulnerabilities field missing from the response json.") 
			if len(res_json["vulnerabilities"]) == 0:
				break
			
			cve_list = res_json["vulnerabilities"]
				
			#preprocess and store updated info
			for cve_info in tqdm(cve_list, desc = "Fetching New"):
				
				if pp.is_cve_invalid(cve_info):
					#TODO: log invalid cve data
					continue
				else:
					#store valid cve 
					cve_id = cve_info["cve"]["id"]
					if cve_id not in unique_cve_ids:
						db.insert_cve(cve_info["cve"])
						unique_cve_ids.append(cve_id)
					else:
						#TODO: log duplicate cve
						continue

			start_indx = start_indx + RESULTS_PER_PAGE

		except Exception as e:
			print("Error: {}".format(e))


if __name__ == '__main__':

	change_start = datetime.now() - timedelta(SYNC_INTERVAL)
	change_end = datetime.now()

	fetch_changes(change_start, change_end)

	fetch_new(change_start, change_end)