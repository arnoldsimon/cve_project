# cve_project

This project is a CVE (Common Vulnerabilities and Exposures) management system that fetches, stores, and displays CVE records using a database, REST API, and a simple UI.

## Project Structure

```
CVE_PROJECT/
├── db_init/         # Database initialization scripts
├── rest_api/        # REST API implementation
├── ui/              # Frontend interface (index.html displays CVEs)
├── venv/            # Virtual environment for dependencies
├── requirements.txt # List of dependencies to be downloaded
```

## How It Works

1. **Database Initialization:**
   - Run `fetchall_cves.py` to fetch and populate the database with the latest CVEs.
   - This step is required only once during the initial setup.

2. **Automatic Updates:**
   - Schedule `sync_changes.py` as a cron job to execute every 6 hours to keep the database updated with new CVEs.

3. **REST API:**
   - The `rest_api/` directory contains code for all API endpoints that serve CVE data.
   - The API provides access to stored CVEs, allowing integration with other systems.

4. **User Interface:**
   - The `ui/index.html` page lists all CVEs stored in the database in a table format.
   - Open this file in a browser to view the data visually.

## Setup and Execution

### 1. Clone the Repository
```sh
git clone https://github.com/your-repo/cve-project.git
cd cve-project
```

### 2. Set Up Virtual Environment
```sh
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Initialize the Database
```sh
python fetchall_cves.py
```

### 5. Schedule Automatic Updates
- Add the following cron job (Linux/macOS) to execute updates every 6 hours:
  ```sh
  0 */6 * * * /path/to/python /path/to/sync_changes.py
  ```
- On Windows, use Task Scheduler to run `sync_changes.py` every 6 hours.

### 6. Run the API Server
```sh
cd rest_api
uvicorn main:app --reload
```

### 7. View the UI
- Open `ui/index.html` in a browser to see the list of CVEs.

## Screenshots
### Input (Fetching CVEs)
![Fetching CVEs](images/intial_fetch.jpg)

### Output (CVE List in UI)
![CVE List](images/cve_list_ui.jpg)