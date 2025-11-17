import psycopg2

hostname = 'localhost'
database = 'dcc2'
username = 'postgres'
pwd = 'deepak'
port_id = 5432

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id
    )
    conn.close()
except Exception as error:
    print(error)