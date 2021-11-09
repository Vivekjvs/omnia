import mysql.connector


def connectdatabase():
  #connectiong to the database
  mydb = mysql.connector.connect(
    host="localhost",
    user="srikar23",
    port = 3305,
    password="Srikar@23",
    database = "codingProfileFeedback"
  )
  #creating a cursor to execute our queries
  mycursor = mydb.cursor()

  return mydb,mycursor

def getUserHandles(userId):
  mydb,mycursor = connectdatabase()

  #quering to retrive all the coding platform handles of particular user with given userid
  selectStatement = f'select codechefHandle,codeforcesHandle,interviewbitHandle,leetCodeHandle,spojHandle from userdetails where userId="{userId}"'
  
  #returning none when there is no such user exists
  try:
    mycursor.execute(selectStatement)
  except Exception as msg:
    print(msg)
    return None

  
  myresult = mycursor.fetchall()
  if(len(myresult) == 0):
    return None
  platforms = ["codechef","codeforces","interviewBit","leetcode","spoj"]
  
  #storing those handles in a dictonary
  res = {}
  for i in range(5):
    res[platforms[i]] = myresult[0][i]

  return res

def updateLeaderBoard(userid,codechefRating,codeforcesRating,interviewBitRating,leetcodeRating,spojRating,overAllRating):
  mydb,mycursor = connectdatabase()

  #checkng whether user exists or not
  mycursor.execute(f"SELECT userid FROM leaderboardTable WHERE userId = '{userid}'")
  data=mycursor.fetchall()
  userdoesntExists = (len(data)==0)

  try:
    if userdoesntExists:
      #inserting the scores of each platform with given data into the database table
      insertStatement = f'insert into leaderboardTable values("{userid}",{codechefRating},{codeforcesRating},{interviewBitRating},{spojRating},{leetcodeRating},{overAllRating})'
      mycursor.execute(insertStatement)
      print("inserted!!")

    else:
      #updating the scores of each platform with given data in the database table
      updataeStatement = f'update leaderboardtable set codechef={codechefRating},codeforces={codeforcesRating},interviewbit={interviewBitRating},spoj={spojRating},leetcode={leetcodeRating},overallScore={overAllRating} where userId="{userid}"'
      mycursor.execute(updataeStatement)
      print("updated!!!")

  except:
    print("Error while updating or inserting")

  mydb.commit()

def getAllUsers():
  mydb,mycursor = connectdatabase()

  #retriving all the registered userIds
  mycursor.execute(f"SELECT userid FROM userdetails")

  return mycursor.fetchall()