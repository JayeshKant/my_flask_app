import cx_Oracle

# Example function to get a connection
def get_db_connection():
    # Adjust DSN, user, and password to your environment
    dsn = cx_Oracle.makedsn("your_db_host", 1521, service_name="YOUR_SERVICE_NAME")
    connection = cx_Oracle.connect(
        user="YOUR_USERNAME",
        password="YOUR_PASSWORD",
        dsn=dsn
    )
    return connection
