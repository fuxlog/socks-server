# Config file for initializing database
import sqlite3


STORAGE = "storage/proxy.db"


def cook(query, params):
    connection = sqlite3.connect(STORAGE)
    cursor = connection.cursor()
    result = cursor.execute(query, params).fetchall()
    print(result)
    connection.close()


def eat(query, params):
    connection = sqlite3.connect(STORAGE)
    cursor = connection.cursor()
    cursor.execute(query, params)
    connection.commit()
    connection.close()


# cook("SELECT * FROM account", ())
# cook("DROP TABLE account", ())
# cook("CREATE TABLE account(username TEXT, password TEXT)", ())
# eat("INSERT INTO account VALUES (?, ?)", ("20205096", "Admin2024@"))
# eat("INSERT INTO account VALUES (?, ?)", ("20200563", "Admin2024@"))
# eat("INSERT INTO account VALUES (?, ?)", ("admin", "Admin2024@"))

