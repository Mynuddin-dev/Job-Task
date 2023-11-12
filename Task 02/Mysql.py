import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user = "root",
    password = "root",
    database = "mydatabase"
)

print(mydb)

# mycursor is an object that allows us to interact with the database
mycursor = mydb.cursor()

# Create a database
# mycursor.execute("CREATE DATABASE mydatabase")

# Show the available databases
# mycursor.execute("SHOW DATABASES")

# ======================= CREATE ===========================
def create_table():
    mycursor.execute("CREATE TABLE IF NOT EXISTS Students (name VARCHAR(255), age INTEGER(10) , id INTEGER AUTO_INCREMENT PRIMARY KEY)")
    mydb.commit()
    print("Table created")

# ======================= INSERT ===========================

def add_students(name, age):
    sql = "INSERT INTO Students (name, age) VALUES (%s, %s)"
    val = (name, age)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")


# ======================= SELECT/READ ===========================
def retrive_students():
    mycursor.execute("SELECT * FROM Students")
    myresult = mycursor.fetchall()
    return myresult

# ======================= UPDATE ===========================
def update_students(id, name, age):
    sql = "UPDATE Students SET name = %s, age = %s WHERE id = %s"
    val = (name, age, id)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) affected")

# ======================= DELETE ===========================
def delete_students(id):
    sql = "DELETE FROM Students WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")

# ======================= CRUD Operation ===========================
create_table()
add_students("Peter", 23)
add_students("Amy", 26)
add_students("Hannah", 28)
add_students("Michael", 30)

print(retrive_students())
update_students(1, "John", 28)
delete_students(2)

