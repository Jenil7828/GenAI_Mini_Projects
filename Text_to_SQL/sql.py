import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

table_info="Create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT);"

cursor.execute(table_info)

cursor.execute("INSERT INTO STUDENT VALUES('Jenil', 'AI', 'B', 9);")
cursor.execute("INSERT INTO STUDENT VALUES('Jinal', 'Microbiology', 'B', 10 );")
cursor.execute("INSERT INTO STUDENT VALUES('Manas', 'Management', 'A', 11);")


print("inserted")

data = cursor.execute('SELECT * FROM STUDENT')

for row in data:
	print(row)

connection.commit()
connection.close()