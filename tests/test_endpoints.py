import requests
from datetime import datetime, timedelta

def test_get_cve_list():
    draw = 1 
    params = {
        'draw': draw
    }
    response = requests.get("http://127.0.0.1:8000/cves/list", params=params)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    response_body = response.json()

    assert "draw" in response_body
    assert "recordsTotal" in response_body
    assert "recordsFiltered" in response_body
    assert "data" in response_body

    assert response_body["draw"] == draw

    for data in response_body["data"]:
        assert "id" in data
        assert "sourceIdentifier" in data
        assert "published" in data
        assert "lastModified" in data
        assert "vulnStatus" in data
        assert "descriptions" in data
        assert "metrics" in data
        assert "configurations" in data


def test_get_cve():
    cve_id = "CVE-2004-1776" 
    params = {
        'cve_id': cve_id
    }
    response = requests.get("http://127.0.0.1:8000/cves/by_id", params=params)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    response_body = response.json()

    assert "id" in response_body
    assert response_body["id"] == cve_id
    assert "sourceIdentifier" in response_body
    assert "published" in response_body
    assert "lastModified" in response_body
    assert "vulnStatus" in response_body
    assert "descriptions" in response_body
    assert "metrics" in response_body
    assert "configurations" in response_body


def test_cve_by_year():
    year = "1988" 
    params = {
        'pub_year': year
    }
    response = requests.get("http://127.0.0.1:8000/cves/by_year", params=params)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    response_body = response.json()

    for data in response_body:
        assert "id" in data
        assert "sourceIdentifier" in data
        assert "published" in data
        assert str(datetime.fromisoformat(data["published"]).year) == year
        assert "lastModified" in data
        assert "vulnStatus" in data
        assert "descriptions" in data
        assert "metrics" in data
        assert "configurations" in data


def test_cve_by_score():
    score = 7.0
    params = {
        'score': score
    }
    response = requests.get("http://127.0.0.1:8000/cves/by_score", params=params)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    response_body = response.json()

    for data in response_body:
        assert "id" in data
        assert "sourceIdentifier" in data
        assert "published" in data
        assert "lastModified" in data
        assert "vulnStatus" in data
        assert "descriptions" in data
        assert "metrics" in data
        assert "cvssMetricV2" in data["metrics"]
        assert "cvssData" in data["metrics"]["cvssMetricV2"]
        assert "baseScore" in data["metrics"]["cvssMetricV2"]["cvssData"]
        assert data["metrics"]["cvssMetricV2"]["cvssData"]["baseScore"] == str(score)
        assert "configurations" in data


def test_cve_by_mod_duration():
    duration = 30
    params = {
        'days': duration
    }
    response = requests.get("http://127.0.0.1:8000/cves/by_mod_duration", params=params)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

    response_body = response.json()

    for data in response_body:
        assert "id" in data
        assert "sourceIdentifier" in data
        assert "published" in data
        assert "lastModified" in data
        assert datetime.now() - datetime.fromisoformat(data["lastModified"]) < timedelta(days=duration)
        assert "vulnStatus" in data
        assert "descriptions" in data
        assert "metrics" in data
        assert "configurations" in data