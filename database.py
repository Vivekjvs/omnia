import mysql.connector


def connectdatabase():
  #connectiong to the database
  mydb = mysql.connector.connect(
    host="localhost",
    user="srikar23",
    port = 3305,
    password="Srikar@23",
    database = "codingprofilesfeedback"
  )
  #creating a cursor to execute our queries
  mycursor = mydb.cursor()

  return mydb,mycursor