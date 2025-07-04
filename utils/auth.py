import psycopg2

# Database connection settings
conn_params = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "vanshvig18",
    "host": "localhost",
    "port": 5432
}

def get_connection():
    return psycopg2.connect(**conn_params)

# Initialize database and create table if it doesn't exist
def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Create a new user
def create_user(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.errors.UniqueViolation:
        return False
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

# Authenticate user login
def authenticate_user(username, password):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = %s", (username,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result and result[0] == password:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error authenticating user: {e}")
        return False
