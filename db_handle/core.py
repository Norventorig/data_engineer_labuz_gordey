from db_handle.db_init import main as db_init
from db_handle.db_gen import main as db_gen


def main(db_config: dict) -> None:
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


if __name__ == '__main__':
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

    main(db_config=database_configuration)
