from sqlalchemy import create_engine, text
import pandas as pd


def main(db_config: dict, output_file: str = "data/result.csv") -> None:
    """
    Creates aggregated csv file.
    :param db_config: dict
    :param output_file: str endswith .csv
    :rtype: None
    """
    sql_query = """
    WITH daily AS (
        SELECT
            DATE(time) AS day,
            COUNT(*) FILTER (WHERE action_type = 'register') AS new_users,
            COUNT(*) FILTER (WHERE action_type = 'post') AS total_posts,
            COUNT(*) FILTER (WHERE action_type = 'post' AND user_id IS NULL) AS anon_posts,
            COUNT(*) FILTER (WHERE action_type = 'create_topic' AND is_success IS TRUE) AS new_topics
        FROM logs
        GROUP BY day
    ),

    final AS (
        SELECT *,
            LAG(new_topics) OVER (ORDER BY day) AS prev_new_topics
        FROM daily
    )

    SELECT
        day,
        new_users,
        total_posts,
        ROUND((anon_posts * 100.0 / NULLIF(total_posts, 0)), 2) AS anon_posts_pct,
        CASE
            WHEN prev_new_topics IS NULL OR prev_new_topics = 0 THEN 0
            ELSE ROUND((new_topics - prev_new_topics) * 100.0 / prev_new_topics, 2)
        END AS topics_growth_pct
    FROM final
    ORDER BY day;
    """

    engine = create_engine(
        f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
    )

    with engine.connect() as con:
        df = pd.read_sql(text(sql_query), con)

    df.to_csv(output_file, index=False)
    print("Saved to CSV")


if __name__ == "__main__":
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
