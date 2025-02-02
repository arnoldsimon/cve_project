
def is_cve_invalid(cve_info):
	is_invalid: bool = False

	if "cve" not in cve_info:
		is_invalid = True
	else:
		if "id" not in cve_info["cve"]:
			is_invalid = True
			
		if "sourceIdentifier" not in cve_info["cve"]:
			is_invalid = True

		if "published" not in cve_info["cve"]:
			is_invalid = True

		if "lastModified" not in cve_info["cve"]:
			is_invalid = True

		if "vulnStatus" not in cve_info["cve"]:
			is_invalid = True

		if "descriptions" not in cve_info["cve"]:
			is_invalid = True
		elif len(cve_info["cve"]["descriptions"]) <= 0:
			is_invalid = True

		if "references" not in cve_info["cve"]:
			is_invalid = True
		elif len(cve_info["cve"]["references"]) <= 0:
			is_invalid = True
	
	return is_invalid
		