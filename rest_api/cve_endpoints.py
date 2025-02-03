from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

import cve_repository as db

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains; you can restrict this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)



@app.get("/cves/list")
async def get_cve_list(start_indx: int = Query(0, ge = 0), length: int = Query(10, ge = 1, le = 100),
					   sort_column: str = Query("lastModified", enum = ["published", "lastModified"]), 
					   sort_order: str = Query("desc", enum = ["asc", "desc"])):
	try:
		res = await db.get_cve_list(start_indx, length, sort_column, sort_order)
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@app.get("/cves/by_id")
async def get_cve(cve_id : str = Query(...)):
	try:
		res = await db.get_cve(cve_id)
		if res is None:
			raise HTTPException(status_code = 404, detail = "CVE with ID: {} not found".format(cve_id))
		
		res["_id"] = str(res["_id"])
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@app.get("/cves/by_year")
async def get_cve_by_year(pub_year: int = Query(..., ge = 1900, le = datetime.now().year)):
	try:
		res = await db.get_cve_by_year(pub_year)
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@app.get("/cves/by_score")
async def get_cve_by_year(score: float = Query(..., ge = 0.1, le = 10.0)):
	try:
		res = await db.get_cve_by_score(score)
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")

@app.get("/cves/by_mod_duration")
async def get_cve_by_mod_duration(days: int = Query(...)):
	try:
		mod_after_date = datetime.now() - timedelta(days = days)
		res = await db.get_cve_by_mod_date(mod_after_date.isoformat())
		return res

	except Exception as e:
		raise HTTPException(status_code = 500, detail = "Internal Server Error.")