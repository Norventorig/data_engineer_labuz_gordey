import psycopg2

import os
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_NAME = os.getenv("DBNAME")
DB_PORT = os.getenv("PORT")


def main():
    try:
        con = psycopg2.connect(database='postgres', user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = con.cursor()
        con.autocommit = True

        cur.execute(f"CREATE DATABASE {DB_NAME}")

    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists")

    except Exception as e:
        print('Error: ', e)

    else:
        print("Database successfully created")

    finally:
        con.close()


if __name__ == "__main__":
    main()