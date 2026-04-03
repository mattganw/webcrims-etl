from database import connect_to_db

def fetch_data():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BEASTLog")
    for row in cursor.fetchall():
        print(row)
    conn.close()

if __name__ == "__main__":
    fetch_data()