from db import get_db

conn = get_db()
cursor = conn.cursor()

cursor.execute("SELECT DATABASE()")
database = cursor.fetchone()

print("Connessione riuscita!")
print("Database:", database[0])

cursor.close()
conn.close()
