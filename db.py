import psycopg2 

def get_connection():
    return psycopg2.connect(
        dbname="docerriebd",
        user="postgres",
        password="pipoca123",
        host="localhost",
    )