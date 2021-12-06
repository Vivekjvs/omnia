import mysql.connector
from database import connectdatabase


#To add the count of each verdict into the database Table
def addToSubmissionsInDb(userId,submissionCount):
  #submissionCount = codeforcesScrap.submissionCount 
  mydb,mycursor = connectdatabase()
  try:
    #Here usersubmissions consists of count of each verdict of particular userId
    insertStatement = f'INSERT INTO usersubmissions VALUES("{userId}",{submissionCount["AcceptedCount"]},{submissionCount["WrongAnswerCount"]},{submissionCount["TimeLimitExceedCount"]},{submissionCount["CompileTimeErrorCount"]},{submissionCount["RuntimeErrorCount"]});'
    mycursor.execute(insertStatement)
  except:
    updateStatement = f'update usersubmissions SET Accepted = {submissionCount["AcceptedCount"]},WrongAnswer = {submissionCount["WrongAnswerCount"]},TimeLimitExceed = {submissionCount["TimeLimitExceedCount"]},CompilationError= {submissionCount["CompileTimeErrorCount"]},RunTimeError= {submissionCount["RuntimeErrorCount"]} where userid="{userId}";'
    mycursor.execute(updateStatement)

  mydb.commit()

  print("addToSubmissionsIntoDb: The submission details are updated")

#Adding the problems of the codeforces into the database
def addToProblemDetails(problemId,problemName,problemLink):
  mydb,mycursor = connectdatabase()
  #problemDetails consists of all the problems that are available in the codeforces
  insertStatement = f'insert ignore into problemDetails values("{problemId}","{problemName}","{problemLink}")'

  try:
    mycursor.execute(insertStatement)
  except:
      pass
  
  mydb.commit()

#To add the problem with respective tags as true into databases under particular userId
def addToUserProblemDetails(valuesList):
  mydb,mycursor = connectdatabase()
  values = f'"{valuesList[0]}","{valuesList[1]}","{valuesList[2]}",'
  values = values+",".join(str(x) for x  in valuesList[3:])

  #userProblemDetails consist of problems submitted by the user
  insertStatement = 'insert ignore into userProblemDetails values(%s)' % values

  try:
    mycursor.execute(insertStatement)
  except Exception as msg:
      #print("Exception Message(addToUserProblemDetails)",msg)
      pass
    
  mydb.commit()

def addToContestDetails(contestid,contestName,contestStartTime):
  mydb,mycursor = connectdatabase()

  #Here contestDetails Table consists of details about all the contests of codeforces
  insertStatement = f'insert ignore into contestDetails values("{contestid}","{contestName}","{contestStartTime}")'

  try:
    mycursor.execute(insertStatement)
  except:
      pass
  
  mydb.commit()

def addToUserContestDetails(userid,platform,contestId,contestRank,contestRating,newRating):
    mydb,mycursor = connectdatabase()
    #userContestDetails Table consists of details about the user participated contests
    insertStatement = f'insert into userContestDetails values("{userid}","{platform}","{contestId}",{contestRank},{contestRating},{newRating})'

    try:
        mycursor.execute(insertStatement)
    except:
        pass
    
    mydb.commit()