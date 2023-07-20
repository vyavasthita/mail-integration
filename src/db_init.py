from mysql.connector import connect, Error, errorcode
from src import env_configuration

config = {
    "host": env_configuration.MYSQL_HOST,
    "database": env_configuration.MYSQL_DB,
    "user": env_configuration.MYSQL_USER,
    "password": env_configuration.MYSQL_PASSWORD,
    "raise_on_warnings": True,
    "autocommit": True,
}


class DBConnection:
    def __init__(self):
        try:
            self.connection = connect(**config)
            self.cursor = self.connection.cursor()
        except Error as error:
            if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(str(error))
        except Exception as error:
            print(str(error))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection.is_connected():
            self.cursor.close()
            # close db connection
            self.connection.close()
