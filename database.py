import mysql.connector


def connectdatabase():
  #connectiong to the database
  mydb = mysql.connector.connect(
    #change credentials before pushing
    host="localhost",
    user="root",
    #change it before pushing
    port = 3306,
    password="4321",
    database = "codingprofilesfeedback"
  )
  #creating a cursor to execute our queries
  mycursor = mydb.cursor()

  return mydb,mycursor