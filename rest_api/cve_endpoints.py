from fastapi import FastAPI, Query, HTTPException
from datetime import datetime, timedelta

import cve_repository as db

app = FastAPI()

@app.get("/get_cve")
async def get_cve(cve_id : str = Query(...)):
	try:
		res = await db.get_cve(cve_id)
		if res is None:
			raise HTTPException(status_code = 404, detail = "CVE with ID: {} not found".format(cve_id))
		
		res["_id"] = str(res["_id"])
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@app.get("/get_cve_by_year")
async def get_cve_by_year(pub_year: int = Query(..., ge = 1900, le = datetime.now().year)):
	try:
		res = await db.get_cve_by_year(pub_year)
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@app.get("/get_cve_by_score")
async def get_cve_by_year(score: float = Query(..., ge = 0.1, le = 10.0)):
	try:
		res = await db.get_cve_by_score(score)
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@app.get("/get_cve_by_mod_duration")
async def get_cve_by_mod_duration(days: int = Query(...)):
	try:
		mod_after_date = datetime.now() - timedelta(days = days)
		res = await db.get_cve_by_mod_date(mod_after_date.isoformat())
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")