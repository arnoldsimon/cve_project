from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

from config import CONFIG

client = AsyncIOMotorClient(CONFIG["db_url"])
db_name = CONFIG["db_name"]
col_name = CONFIG["col_name"]

collection = client[db_name][col_name]

#TODO: log errors

async def get_cve_list(start_indx: int, length: int, sort_column: str, sort_order: str, draw: int):
	try:
		is_asc = 1 if sort_order == "asc" else -1

		total_docs = await collection.count_documents({})
		db_res = collection.find().skip(start_indx).limit(length).sort(sort_column, is_asc)
		cve_list = await db_res.to_list()

		for cve in cve_list:
			cve["_id"] = str(cve["_id"])
		
		res = {
			"draw" : draw,
			"recordsTotal" : total_docs,
			"recordsFiltered" : total_docs,
			"data" : cve_list
		}

		return res

	except Exception as e:
		raise e

async def get_cve(cve_id: str):
	try:
		res = await collection.find_one({ 'id' : cve_id })
		return res
	except Exception as e:
		raise e
		
async def get_cve_by_year(pub_year: int):
	try:
		start_year = datetime(pub_year, 1, 1, 0, 0, 0, tzinfo = timezone.utc).isoformat()
		end_year = datetime(pub_year + 1, 1, 1, 0, 0, 0, tzinfo = timezone.utc).isoformat()

		db_res = collection.find({ 'published' : { '$gte' : start_year, '$lt' : end_year} })
		res = await db_res.to_list()

		for cve in res:
			cve["_id"] = str(cve["_id"])

		return res

	except Exception as e:
		raise e

async def get_cve_by_score(score: float):
	try:
		filter = {
			"$or": [
                {"metrics.cvssMetricV3.cvssData.baseScore": score },  
                {"metrics.cvssMetricV2.cvssData.baseScore": score }  
            ]
		}
		db_res = collection.find(filter)
		res = await db_res.to_list()

		for cve in res:
			cve["_id"] = str(cve["_id"])

		return res

	except Exception as e:
		raise e

async def get_cve_by_mod_date(mod_date: datetime):
	try:
		db_res = collection.find({ "lastModified" : {"$gt" : mod_date}})
		res = await db_res.to_list()

		for cve in res:
			cve["_id"] = str(cve["_id"])

		return res

	except Exception as e:
		raise e