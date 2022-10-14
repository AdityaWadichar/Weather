import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE Cities (name TEXT)')
print("Table created successfully")
conn.close()