## Features
- PyAutoGUI automation script to navigate and scrape the NYS WebCriminal court calendar.
- Backend service to store extracted court data in a Microsoft SQL Server (MSSQL) database.
- Handles record lifecycle changes, including updates, additions, and deletions.

## Installation and Setup
1. Clone this repository:

```bash
git clone https://github.com/mattganw/webcrims-etl.git
cd webcrims-etl
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

Copy .env.example and create a .env file in the project root:

```bash
# Court name to scrape (leave empty for all courts)
COURT_NAME=Suffolk 1st District Court

# Number of days to look ahead (must be >= 0)
NUM_DAYS=3

# Wait time in seconds for court calendar load (must be >= 15)
WAIT_TIME=15

# Database connection string (required for DB operations)
DB_CONNECTION_STRING=<your_mssql_connection_string_here>
```

4. Run pipeline using Python:

```bash
python main.py
```



