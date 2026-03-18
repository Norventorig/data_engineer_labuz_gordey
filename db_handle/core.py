from db_init import main as db_init
from db_gen import main as db_gen

import os
from dotenv import load_dotenv

load_dotenv()


db_config = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}

if __name__ == '__main__':
    try:
        if None in db_config.values():
            raise Exception("Please provide database configuration")

    except Exception as e:
        print('Error: ', e)

    else:
        db_init(db_config=db_config)
        db_gen(db_config=db_config)

    finally:
        print('db_handle/core.py script finished')
