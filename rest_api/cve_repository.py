from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone, timedelta

from config import CONFIG

client = AsyncIOMotorClient(CONFIG["db_url"])
db_name = CONFIG["db_name"]
col_name = CONFIG["col_name"]

collection = client[db_name][col_name]

#TODO: log errors

async def get_cve_list(start_indx: int, length: int, sort_column: str, sort_order: str, draw: int, cve_id, cve_score, last_mod):
	try:
		is_asc = 1 if sort_order == "asc" else -1

		filter = {}
		if cve_id:
			filter["id"] = cve_id
		if cve_score:
			filter["metrics.cvssMetricV2"] = {
				"$elemMatch" : {
					"cvssData.baseScore" : cve_score
				}
			}
		if last_mod:
			mod_after_date = datetime.now() - timedelta(days = last_mod)
			filter["lastModified"] = {
				"$gt" : mod_after_date.isoformat()
			}

		total_docs = await collection.count_documents(filter)
		db_res = await collection.find(filter).skip(start_indx).limit(length).sort(sort_column, is_asc).to_list()

		for cve in db_res:
			cve["_id"] = str(cve["_id"])
		
		res = {
			"draw" : draw,
			"recordsTotal" : total_docs,
			"recordsFiltered" : total_docs,
			"data" : db_res
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