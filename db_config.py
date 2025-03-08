import sqlite3

def get_db_connection():
    # This will create a file-based SQLite database (test.db) in your project folder.
    connection = sqlite3.connect("test.db")
    connection.row_factory = sqlite3.Row
    return connection
