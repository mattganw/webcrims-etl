## Features
- PyAutoGUI automation script to navigate and scrape the NYS WebCriminal court calendar.
- Backend service to store extracted court data in a Microsoft SQL Server (MSSQL) database.
- Handles record lifecycle changes, including updates, additions, and deletions.

## Installation and Setup
1. Clone this repository

```bash
git clone https://github.com/mattganw/webcrims-etl.git
cd webcrims-etl
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Set up environment variable

Create a .env file in the project root:

```bash
DB_CONNECTION_STRING=<your_connection_string>
```

4. Run pipeline

```bash
python3 main.py
```



