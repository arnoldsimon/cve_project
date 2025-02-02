import requests

import preprocess_helper 	as pp
import database_helper 		as db

base_url : str = "https://services.nvd.nist.gov/rest/json/cves/2.0"

results_per_page : int = 5

unique_cve_ids : list = []

# fetch -> preprocess -> store

def fetch_batch(start_indx: int):
	try:
		parameters = {
			'startIndex' : start_indx,
			'resultsPerPage' : results_per_page
		}
		response = requests.get(base_url, params=parameters)
		response.raise_for_status()
		if response.headers.get("Content-Type") == "application/json":
			return response.json()
		else:
			return None

	except requests.exceptions.RequestException as e:
		print("Error: {}".format(e))
		return None


#check for mandatory fields -> remove duplicates -> perform data integrity check -> data cleaning
def preprocess(cve_info):
	global unique_cve_ids

	#perform field validation on cve data
	if pp.is_cve_invalid(cve_info) == False:
		cve_id = cve_info["cve"]["id"]

		#remove duplicate cve data
		if cve_id not in unique_cve_ids:
			unique_cve_ids.append(cve_id)
			#TODO: data integrity
			#TODO: data cleaning
			return cve_info

	#if cve data is invalid return None
	return None


def store_data(cve_info):
	db.insert_cve(cve_info["cve"])


if __name__ == '__main__':

	start_indx: int = 0

	db.drop_db()
	for i in range(2):
		data = fetch_batch(start_indx)

		if data is None:
			break
		elif "vulnerabilities" not in data:
			break
		elif len(data["vulnerabilities"]) == 0:
			break

		for cve_info in data["vulnerabilities"]:
			cve_info = preprocess(cve_info)
			if cve_info is None:
				continue
			store_data(cve_info)

		start_indx = start_indx + results_per_page