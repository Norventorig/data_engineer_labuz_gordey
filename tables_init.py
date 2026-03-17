import psycopg2

import os
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_NAME = os.getenv("DBNAME")
DB_PORT = os.getenv("PORT")

try:
    with psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) as con:
        cur = con.cursor()

        # Таблица users хранит информацию о пользователях. На данный момент только id и имя.
        cur.execute("CREATE TABLE IF NOT EXISTS users "
                    "(id SERIAL PRIMARY KEY, username VARCHAR (40))")

        # Таблицу логов я решил не делать отдельной таблицей для каждого типа действия.
        # log_id - идентификатор записи в таблице;
        # user_id – пользователь, который совершает действие;
        # action_type - тип совершенного действия (visit/register/login/logout/create_topic/view_topic/delete_topic/post);
        # entity_id — сущность, над которой выполняется операция (например id созданного поста);
        # is_success- успешное ли было завершение операции или нет;
        # time - дата действия.
        cur.execute("CREATE TABLE IF NOT EXISTS logs "
                    "(log_id SERIAL PRIMARY KEY, user_id INT REFERENCES users(id), "
                    "action_type VARCHAR(30), entity_id INT NULL, is_success BOOLEAN, time TIMESTAMP")

        # Я решил не создавать таблицу для entities, так как это будет избыточно и не требуется в тз.
        # Также для каждой типа придется создавать свою таблицу и логику.

except Exception as e:
    print('Error:', e)

else:
    print(f'Tables created successfully')
