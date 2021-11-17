from database import connectdatabase
import scores,codeforcesScrap

def isValidAdmin(userId,Password):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select userid,password from admindetails where userId="{userId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        print(msg)
        return None

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return "user doesn't exists"
    
    if(myresult[0][1] != Password):
        return "wrong Password"
    else:
        return "successfull"

def addAdmin(adminId,password,email):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select userid,password from admindetails where userId="{adminId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        print(msg)
        return None

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
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
        print(msg)
        return "Error"

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return "user doesn't exists"
    
    if(myresult[0][1] != password):
        return "wrong Password"
    else:
        return "successfull"
    
def addStudent(adminId,password,codechef,codeforces,InterviewBit,spoj,leetcode,email,phone):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select userId,userpassword from userdetails where userId="{adminId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        print(msg)
        return "Error"

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        insertStatement = f'insert Ignore into userdetails(userId,userPassword,codechefHandle,codeforcesHandle,interviewbitHandle,spojHandle,leetCodeHandle,email,phone) values("{adminId}","{password}","{codechef}","{codeforces}","{InterviewBit}","{spoj}","{leetcode}","{email}","{phone}")'
  
        #returning none when there is no such user exists
        try:
            mycursor.execute(insertStatement)
        except Exception as msg:
            print(msg)
            return "failed!!"
        mydb.commit()
        scores.updateScore()
        codeforcesScrap.main(adminId)
        return "Successfull!!!"
    else:
        return "User Aleady Exists"

