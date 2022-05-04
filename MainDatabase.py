from database import connectdatabase
import scores,codeforcesScrap
from encryption import *

def isValidAdmin(adminId,Password):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select adminId,password from admindetails where adminId="{adminId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        #print(msg)
        return None

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return "user doesn't exists"
    
    if(not check_password(Password,myresult[0][1])):
        return "wrong Password"
    else:
        return "successfull"

def addAdmin(adminId,password,email):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select adminId,password from admindetails where adminId="{adminId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        print(msg)
        return "Error"

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        password = get_hashed_password(password)
        insertStatement = f'insert Ignore into adminDetails values("{adminId}","{password}","{email}")'
  
        #returning none when there is no such user exists
        try:
            mycursor.execute(insertStatement)
        except Exception as msg:
            print(msg)
            return "failed!!"
        mydb.commit()
        return "Successfull!!!"
    else:
        return "User Aleady Exists"


def isValidStudent(userId,password):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select userid,userPassword from userDetails where userId="{userId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        #print(msg)
        return "Error"

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return "user doesn't exists"
    
    if(not check_password(password,myresult[0][1])):
        return "wrong Password"
    else:
        return "successfull"
    
def addStudent(userId,name,branch,cgpa,backlogs,yop,password,codechef,codeforces,InterviewBit,spoj,leetcode,email,phone):
    mydb,mycursor = connectdatabase()
    password = get_hashed_password(password)

    selectStatement = f'select userId,userpassword from userdetails where userId="{userId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        #print(msg)
        return "Error"

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        insertStatement = f'insert Ignore into userdetails(userId,name,branch,gpa,backlogs,passedOut,userPassword,codechefHandle,codeforcesHandle,interviewbitHandle,spojHandle,leetCodeHandle,email,phone) values("{userId}","{name}","{branch}",{cgpa},{backlogs},{yop},"{password}","{codechef}","{codeforces}","{InterviewBit}","{spoj}","{leetcode}","{email}","{phone}")'
  
        #returning none when there is no such user exists
        try:
            mycursor.execute(insertStatement)
        except Exception as msg:
            print(msg)
            return "failed!!"
        mydb.commit()
        scores.updateScore()
        codeforcesScrap.main(userId)
        return "Successfull!!!"
    else:
        return "User Aleady Exists"

def updateStudentPassword(userid,Password):
    mydb,mycursor = connectdatabase()

    Password = get_hashed_password(Password)
    selectStatement = f'update userdetails set userpassword = "{Password}" where userId="{userid}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
        mydb.commit()
    except Exception as msg:
        #print(msg)
        return "couldn't update user password Please try again!!!"
    return "True"

def isValidStudentEmail(email):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select userid from userDetails where email="{email}"'
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        #print(msg)
        return False

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return "user doesn't exists"
    return True