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
    db_init(db_config=db_config)
    db_gen(db_config=db_config)
