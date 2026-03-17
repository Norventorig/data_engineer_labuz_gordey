from typing import Any

import psycopg2
import numpy as np
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_NAME = os.getenv("DBNAME")
DB_PORT = os.getenv("PORT")


def drop_old_data() -> None:
    """
    Deletes old records
    :rtype: None
    """
    try:
        with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) as con:
            cur = con.cursor()

            cur.execute("DELETE FROM logs")
            cur.execute("DELETE FROM users")

    except Exception as e:
        print('Error: ', e)

    else:
        print("Old data deleted successfully")


def users_generation(num_users: int = 20) -> None:
    """
    Generates specified number of new Users
    :rtype: None
    :param num_users:
    """
    users_data = [(f'User{i}', datetime.now() - timedelta(days=np.random.randint(1, 28))) for i in
                  range(1, num_users + 1)]

    try:
        with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) as con:
            cur = con.cursor()

            cur.executemany(query="INSERT INTO users (username, created_at) VALUES (%s, %s)", vars_list=users_data)

    except Exception as e:
        print('Error: ', e)

    else:
        print("Users generated successfully")


def get_user_ids() -> list[int] | None:
    """
    Returns a List containing all User IDs
    :rtype: list[int] | None
    :return: user_ids
    """
    try:
        with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) as con:
            cur = con.cursor()

            cur.execute("SELECT id FROM users")
            user_ids = [row[0] for row in cur.fetchall()]

    except Exception as e:
        print('Error: ', e)

    else:
        print("IDs were retrieved successfully")
        return user_ids


def logs_generation(user_ids: list[int],
                    actions: list[str] = None,
                    start_date: datetime = datetime(2026, 3, 1),
                    num_days: int = 30) -> None:
    """
    Generates logs
    :rtype: None
    :param actions: list[str]
    :param user_ids: list[int]
    :param start_date: datetime
    :param num_days: int
    """
    if actions is None:
        actions = ['visit', 'register', 'login', 'logout', 'create_topic', 'view_topic', 'delete_topic', 'post']

    try:
        with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) as con:
            cur = con.cursor()

            for day in range(num_days):
                current_day = start_date + timedelta(days=day)

                for action in actions:
                    n_actions = np.random.randint(5, 10)

                    for _ in range(n_actions):
                        user_id = None if np.random.random() < 0.5 else int(np.random.choice(user_ids))
                        is_success = False if action in ['create_topic', 'delete_topic'] and not user_id else True
                        entity_id = np.random.randint(1, 500) \
                            if action in ['create_topic', 'view_topic', 'delete_topic','post'] else None
                        timestamp = current_day + timedelta(seconds=np.random.randint(0, 86399))

                        cur.execute("INSERT INTO logs (user_id, action_type, entity_id, is_success, time) "
                                    "VALUES (%s, %s, %s, %s, %s)",
                            (user_id, action, entity_id, is_success, timestamp))

    except Exception as e:
        print('Error: ', e)

    else:
        print("Logs generated successfully")


def main():
    drop_old_data()
    users_generation()
    logs_generation(user_ids=get_user_ids())


if __name__ == '__main__':
    main()
