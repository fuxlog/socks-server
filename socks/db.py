import sqlite3
from .utils import validate_username, validate_password


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
        return False
    
    if not validate_username(username):
        return False
    
    if not validate_password(password):
        return False
    
    
    connection = sqlite3.connect(STORAGE)
    cursor = connection.cursor()
    query = "INSERT INTO account (username, password) VALUES (?, ?)"
    params = (username, password)
    cursor.execute(query, params)
    connection.commit()
    connection.close()
    return True


def verify_account(username, password):
    account = find_account_by_username(username)
    if account is None:
        return False
    else:
        if account.password == password:
            return True
        else:
            return False



def change_password(username, new_password):
    account = find_account_by_username(username)
    if account is None:
        return False
    if validate_password(new_password) is False:
        return False
    else:
        connection = sqlite3.connect(STORAGE)
        cursor = connection.cursor()
        query = "UPDATE account SET password = ? WHERE username = ?"
        params = (new_password, username)
        cursor.execute(query, params)
        connection.commit()
        connection.close()
        return True