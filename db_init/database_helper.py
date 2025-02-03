from pymongo import MongoClient
from datetime import datetime

from config import CONFIG


client_url 	= CONFIG["db_url"]
db_name 	= CONFIG["db_name"]
col_name 	= CONFIG["col_name"]


def drop_db():
	with MongoClient(client_url) as client:
		client.drop_database(db_name)

def read_cve(cve_id):
	pass

def delete_cve(cve_id):
	pass

def insert_cve(cve_data):

	cve_data["created_on"] = datetime.now()
	cve_data["updated_on"] = datetime.now()

	with MongoClient(client_url) as client:
		collection = client[db_name][col_name]
		result = collection.insert_one(cve_data)

def update_cve(cve_id, cve_data):

	cve_data["updated_on"] = datetime.now()

	with MongoClient(client_url) as client:
		collection = client[db_name][col_name]
		result = collection.update_one({ 'id' : cve_id }, { '$set' : cve_data })