from functools import wraps
from src.data_layer.db_connection import DBConnection


def check_db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(
            f"Checking if we are connected to database. Request coming from {func.__name__}."
        )

        with DBConnection() as db_connection:
            if db_connection.connection.is_connected():
                print("Congratulations!. Db connection is successful.")

        return func(*args, **kwargs)

    return wrapper
