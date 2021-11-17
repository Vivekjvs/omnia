from database import connectdatabase

def isValidAdmin(userId,Password):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select userid,password from adminDetails where userId="{userId}"'
  
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

    selectStatement = f'select userid,password from adminDetails where userId="{adminId}"'
  
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
    
def addStudent(userId,password,codechef,codeforces):
    mydb,mycursor = connectdatabase()

    selectStatement = f'select userId,userpassword from userdetails where userId="{userId}"'
  
    #returning none when there is no such user exists
    try:
        mycursor.execute(selectStatement)
    except Exception as msg:
        print(msg)
        return "Error"

    
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        insertStatement = f'insert Ignore into userdetails(userId,userPassword,codechefHandle,codeforcesHandle) values("{userId}","{password}","{codechef}","{codeforces}")'
  
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

