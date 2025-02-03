import requests
from tqdm import tqdm

from config import CONFIG
import preprocess_helper as pp
import database_helper as db

BASE_URL : str 			= CONFIG["fetch_url"]
RESULTS_PER_PAGE : int 	= CONFIG["results_per_page"] 


def fetch_all():

	start_indx : int = 0
	unique_cve_ids : list = []
	while True:
		try:
			params = {
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
			for cve_info in tqdm(cve_list, desc = "Fetching"):
				
				if pp.is_cve_invalid(cve_info):
					#log invalid cve data
					#print("invalid cve: {}".format(cve_info["cve"]))
					continue
				else:
					#store valid cve 
					cve_id = cve_info["cve"]["id"]
					if cve_id not in unique_cve_ids:
						db.insert_cve(cve_info["cve"])
						unique_cve_ids.append(cve_id)
					else:
						#TODO: log duplicate cve info
						continue
			
			start_indx = start_indx + RESULTS_PER_PAGE

		except Exception as e:
			print("Error: {}".format(e))

	print("All data fetched successfully!")


if __name__ == '__main__':

	db.drop_db()
	fetch_all()