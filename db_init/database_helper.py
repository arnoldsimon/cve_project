from pymongo import MongoClient


client_url 	= "mongodb://localhost:27017"
db_name 	= "cve_project"
col_name 	= "nvd_cves"


def drop_db():
	with MongoClient(client_url) as client:
		client.drop_database(db_name)

def read_cve(cve_id):
	pass

def delete_cve(cve_id):
	pass

def insert_cve(cve_data):
	with MongoClient(client_url) as client:
		collection = client[db_name][col_name]
		result = collection.insert_one(cve_data)

def update_cve(cve_data):
	pass