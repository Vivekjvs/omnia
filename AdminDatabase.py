from database import connectdatabase


def getUserHandles(userId):
  mydb,mycursor = connectdatabase()

  #quering to retrive all the coding platform handles of particular user with given userid
  selectStatement = f'select codechefHandle,codeforcesHandle,interviewbitHandle,leetCodeHandle,spojHandle from userdetails where userId="{userId}"'
  
  #returning none when there is no such user exists
  try:
    mycursor.execute(selectStatement)
  except Exception as msg:
    #print(msg)
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

def updateLeaderBoard(userid,codechefRating,codeforcesRating,interviewBitRating,leetcodeRating,spojRating,overAllRating,currentDate):
  mydb,mycursor = connectdatabase()

  try:
      #inserting the scores of each platform with given data into the database table
      insertStatement = f'insert ignore into leaderboardTable values("{userid}",{codechefRating},{codeforcesRating},{interviewBitRating},{spojRating},{leetcodeRating},{overAllRating},"{currentDate}")'
      mycursor.execute(insertStatement)
      #print("inserted!!")
  except:
    pass
    #print("Error while inserting")

  mydb.commit()

def getAllUsers():
  mydb,mycursor = connectdatabase()

  #retriving all the registered userIds
  mycursor.execute(f"SELECT userid FROM userdetails")

  return mycursor.fetchall()