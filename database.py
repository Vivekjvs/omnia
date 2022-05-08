import mysql.connector


def connectdatabase():
  #connectiong to the database
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    port = 3306,
    password="4321",
    database = "codingprofilesfeedback"
  )
  #creating a cursor to execute our queries
  mycursor = mydb.cursor()

  return mydb,mycursor