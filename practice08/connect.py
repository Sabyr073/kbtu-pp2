import psycopg2
from config import load_config

def connect():
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            print("Connected to PostgreSQL successfully")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    connect()