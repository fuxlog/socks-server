import sqlite3


STORAGE = "storage/proxy.db"


class Account:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def find_account_by_username(username: str) -> Account:
    connection = sqlite3.connect(STORAGE)
    cursor = connection.cursor()
    query = "SELECT username, password FROM account WHERE username = ?"
    params = (username,)
    result = cursor.execute(query, params).fetchone()
    if result is None:
        connection.close()
        return None
    else:
        username, password= result
        connection.close()
        return Account(username, password)


def save_account(username: str, password: str) -> int:
    account = find_account_by_username(username)
    if account is not None:
        return 2
    
    connection = sqlite3.connect(STORAGE)
    cursor = connection.cursor()
    query = "INSERT INTO account (username, password) VALUES (?, ?)"
    params = (username, password)

    result = cursor.execute(query, params)
    connection.commit()
    connection.close()
    return 1


def save_account1(username: str, password: str) -> Account:
    connection = sqlite3.connect(STORAGE)
    cursor = connection.cursor()
    query = "INSERT INTO account (username, password) VALUES (?, ?)"
    params = (username, password)

    if find_account_by_username(username) is not None:
        connection.close()
        return None

    result = cursor.execute(query, params)
    connection.commit()
    connection.close()
    return Account(result[0], result[1], result[2], result[3])


def verify_account(username, password):
    account = find_account_by_username(username)
    if account is None:
        return False
    else:
        if account.password == password:
            return True
        else:
            return False
