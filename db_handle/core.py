from db_init import main as db_init
from tables_init import main as tables_init
from db_gen import main as db_gen


if __name__ == '__main__':
    db_init()
    tables_init()
    db_gen()
