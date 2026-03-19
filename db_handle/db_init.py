import psycopg2


def init_db(db_config: dict) -> None:
    """
    Initializes the database with a given configuration without any data and tables
    :param db_config: dict
    :rtype: None
    """
    try:
        admin_config = db_config.copy()
        admin_config["dbname"] = "postgres"

        con = psycopg2.connect(**admin_config)
        cur = con.cursor()
        con.autocommit = True

        cur.execute(f"CREATE DATABASE {db_config['dbname']}")

    except psycopg2.errors.DuplicateDatabase:
        print("Database already exists")

    except Exception as e:
        print('Error: ', e)

    else:
        print("Database successfully created")

    finally:
        con.close()


def init_tables(db_config: dict) -> None:
    """
    Initialize all required tables for database
    :param db_config: dict
    :rtype: None
    """
    try:
        with psycopg2.connect(**db_config) as con:
            cur = con.cursor()

            # Таблица users хранит информацию о пользователях. На данный момент только id и имя.
            cur.execute("CREATE TABLE IF NOT EXISTS users "
                        "(id SERIAL PRIMARY KEY, username VARCHAR(50), created_at TIMESTAMP)")

            # Таблицу логов я решил не делать отдельной таблицей для каждого типа действия.
            # log_id - идентификатор записи в таблице;
            # user_id – пользователь, который совершает действие;
            # action_type - тип совершенного действия (visit/register/login/logout/create_topic/view_topic/delete_topic/post);
            # entity_id — сущность, над которой выполняется операция (например id созданного поста);
            # is_success- успешное ли было завершение операции или нет;
            # time - дата действия.
            cur.execute("CREATE TABLE IF NOT EXISTS logs "
                        "(log_id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), "
                        "action_type VARCHAR(30), entity_id INT NULL, is_success BOOLEAN, time TIMESTAMP)")

            # Я решил не создавать таблицу для entities, так как это будет избыточно и не требуется в тз.
            # Также для каждой типа придется создавать свою таблицу и логику.

    except Exception as e:
        print('Error:', e)

    else:
        print(f'Tables created successfully')


def main(db_config: dict) -> None:
    init_db(db_config=db_config)
    init_tables(db_config=db_config)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    database_config = {
        "dbname": os.getenv("DBNAME"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
    }

    main(db_config=database_config)
