import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="vanshvig18",
        host="localhost",
        port="5432"
    )
    print("✅ Connected successfully")
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)

