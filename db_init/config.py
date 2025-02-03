
CONFIG = {
	'fetch_url' : "https://services.nvd.nist.gov/rest/json/cves/2.0",

	'results_per_page' : 1000,
	'sync_interval' : 6,

	'db_url' : "mongodb://localhost:27017",
	'db_name' : "cve_project",
	'col_name' : "nvd_cves"
}