from db_handle.core import main as db_main
from aggregation import main as aggregation_main


import os
from dotenv import load_dotenv
load_dotenv()


database_configuration = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}

try:
    db_main(db_config=database_configuration)
    aggregation_main(db_config=database_configuration)

except Exception as e:
    print(e)

finally:
    print('THIS IS THE END')
