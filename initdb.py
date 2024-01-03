import sqlite3


connection = sqlite3.connect("storage/proxy.db")
cursor = connection.cursor()
# cursor.execute("CREATE TABLE account(username TEXT, password TEXT)")
# cursor.execute("INSERT INTO account VALUES ('admin', 'admin2024')")
result = cursor.execute("SELECT username, password FROM account").fetchall()
print(result)

connection.close()