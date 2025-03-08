from db_config import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Create a users table if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
""")
conn.commit()
conn.close()
print("Database initialized.")
