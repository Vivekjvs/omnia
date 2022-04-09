import mysql.connector


def connectdatabase():
  #connectiong to the database
  mydb = None
  if(mydb is None):
    mydb = mysql.connector.connect(
      #change credentials before pushing
      host="localhost",
      user="srikar23",
      #change it before pushing
      port = 3305,
      password="Srikar@23",
      database = "codingprofilesfeedback"
    )
  #creating a cursor to execute our queries
  mycursor = mydb.cursor()

  return mydb,mycursor