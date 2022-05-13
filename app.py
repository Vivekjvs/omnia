from fileinput import filename
import os
from flask import Flask,request,redirect,session,flash,render_template,send_file
from flask.helpers import url_for
from mysqlx import Statement
from MainDatabase import *
from flask.templating import render_template
import threading,time
from scores import updateScore
from datetime import date, timedelta, datetime
from codeforcesProblems_ContestDetails import updateCodeforcesProblems_Contests
from ActiveContests import getActiveContests
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail,Message
import openpyxl

app = Flask(__name__)
app.secret_key = "loveYou3000"
app.permanent_session_lifetime = timedelta(days=2)
app.config['hello'] = "hello"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('email_id')
app.config['MAIL_PASSWORD'] = os.environ.get('email_password')
mail = Mail(app)


currentDate = date.today().strftime("%Y-%m-%d")

@app.route('/')
def home():
    return render_template('home.html') 

#Faculty Portal
@app.route('/fac_login.html')
def facultyLogin():
    #checking wheather faculty/student already logged in
    if session.get("faculty") is not None:
        return redirect('/FacultyDashboard')
    if session.get("user") is not None:
        return redirect("/")
    return render_template('fac_login.html')

@app.route('/fac_login.html/validate', methods =["GET", "POST"])
def facultyValidate():
    if request.method == "POST":
        # getting input with name = user_name in HTML form 
        adminId = request.form.get("user_name")
        # getting input with name = password in HTML form 
        password = request.form.get("password")

        verdict =  isValidAdmin(adminId,password)#Authenticating..
        if(verdict == "successfull"):
            session["faculty"] = adminId #added to session
            session.permanent = True
            return redirect('/FacultyDashboard')
        return f'<h2>{verdict}!!!</h2>' #for Incorrect credentials
    return "Sorry!!"

@app.route('/FacultyDashboard')
def Facdashboard():
    if session.get("faculty") is not None:
        mydb,mycursor = connectdatabase()

        selectStatement = f'select userId,overallScore from leaderboardtable where ScoredDate="{currentDate}" order by overallScore DESC limit 3'
        mycursor.execute(selectStatement+";")
        top3Scorers = tuple(mycursor.fetchall())

        past30Days = (datetime.now() - timedelta(30)).strftime("%Y-%m-%d")
        past30Statement = f'select userId,overallScore from leaderboardtable where ScoredDate="{past30Days}"'
        maxStreakStatement = f'select a.userId as userId,a.overallScore-b.overallScore as overallScore from ({selectStatement}) as a inner join ({past30Statement}) as b on a.userId=b.userId order by overallScore DESC limit 3;'
        
        mycursor.execute(maxStreakStatement)
        recentTop3 = tuple(mycursor.fetchall())

        return render_template('FacHomePage.html',data= top3Scorers,data2 = recentTop3)
    return redirect('/')

@app.route('/fac_register.html', methods =["GET", "POST"])
def facultySignUp():
    return render_template('fac_register.html')

@app.route('/fac_register.html/validate', methods =["GET", "POST"])
def facultyRegistration():
    if request.method == "POST":
        adminId = request.form.get("user_name")# getting input with name = user_name in HTML form 
        password = request.form.get("password")# getting input with name = password in HTML form 
        email = request.form.get("email") # getting input with name = email  in HTML form 

        status =  addAdmin(adminId,password,email)
        if(status == "Successfull!!!"):
            return redirect('/fac_login.html')
        return status
    return "Sorry"

@app.route('/ChangeUserPassword')
def ChangeUserPassByAdmin():
    if session.get("faculty") is not None:
        return render_template('/changeUserPassByAdmin.html')
    return redirect("/")

@app.route('/ChangeUserPassword/validate',methods =["GET", "POST"])
def ChangeUserPassByAdminValidate():
    if request.method == "POST" and session.get("faculty") is not None:
        userId = request.form.get("user")# getting input with name = password in HTML form
        status = isValidStudent(userId,"")#authenticating...
        if status != "user doesn't exists":
            updateStatus = updateStudentPassword(userId,"12345")
            if updateStatus != "True":
                return updateStatus
            else:
                flash('User Password changed Successfully!!!','success')
                return redirect('/adminLeaderboard')
        else:
            return status
    return redirect("/logout")
    
@app.route('/Comapnies', methods =["GET", "POST"])
def AdminComapnies():
    if session.get("faculty") is not None:
        mydb,mycursor = connectdatabase()
        countOfTR = 'select count(*) from placements as b where b.company_name = a.name and b.package = a.package and b.level_of_clearence in ("TR","HR")'
        countOfPlace = 'select count(*) from placements as b where b.company_name = a.name and b.package = a.package and b.level_of_clearence = "CLR"'
        statement = f'select a.company_id,a.name,a.package, ({countOfTR}) as interviewCount,({countOfPlace}) as Cleared ,CASE WHEN a.campus_hiring THEN "On-Campus" ELSE "Off-Campus" END as placement from company as a;'
        mycursor.execute(statement)
        data = mycursor.fetchall()
        data = tuple(data)

        return render_template('admin_companies.html',data = data)
    return redirect('/')

@app.route('/adminLeaderboard', methods =["GET", "POST"])
def admintable():
    if session.get("faculty") is not None:
        mydb,mycursor = connectdatabase()
        statement = f'select a.userId,b.phone,b.email,a.codechef,a.codeforces,a.interviewbit,a.spoj,a.leetcode,a.overallScore from leaderboardtable as a inner join userdetails as b on a.userId = b.userId where scoredDate="{currentDate}" order by a.overallScore desc,a.userId'
        mycursor.execute(statement)
        data = mycursor.fetchall()
        data = tuple(data)
        headings = ("Roll No.","Phone","email","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")

        return render_template('admin_leaderboard.html',headings=headings,data=data,filterStatus= True)
    return redirect('/')

@app.route('/adminLeaderboardFilter', methods =["GET", "POST"])
def adminFiltertable():
    if session.get("faculty") is not None:
        mydb,mycursor = connectdatabase()
        if request.method == "POST":
            startDate = request.form.get("startDate")# getting input with name = user_name in HTML form 
            endDate = request.form.get("endDate")# getting input with name = password in HTML form
            
            #records according to start date
            startStatement = f'select userId,codechef,codeforces,interviewbit,spoj,leetcode,overallScore from leaderboardtable where scoredDate="{startDate}"'
            #records according to end date
            endStatement = f'select userId,codechef,codeforces,interviewbit,spoj,leetcode,overallScore from leaderboardtable where scoredDate="{endDate}"'
            #scored between start and end date
            currentStatement = f'select a.userid as userId,b.codechef-a.codechef as codechef,b.codeforces-a.codeforces as codeforces, b.interviewbit-a.interviewbit as interviewbit, b.spoj-a.spoj as spoj, b.leetcode-a.leetcode as leetcode, b.overallScore-a.overallScore as overallScore from ({startStatement}) as a,({endStatement}) as b where a.userId=b.userId'

            finalStatement = f'select c.userId,d.phone,d.email,c.codechef,c.codeforces,c.interviewbit,c.spoj,c.leetcode,c.overallScore from ({currentStatement}) as c inner join userdetails as d on c.userId = d.userId order by c.overallScore desc, c.userId'
            
            headings = ("Roll No.","Phone","email","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")
            

            mycursor.execute(finalStatement)
            data = mycursor.fetchall()
            data = tuple(data)

            return render_template('admin_leaderboard.html',headings=headings,data=data,filterStatus=True)
    return redirect('/')

@app.route('/Faculty/CRTstatistics')
def CrtStatistics():
    if session.get("faculty") is not None:
        mydb,mycursor = connectdatabase()

        countOfClearedStatement = 'select count(*) from placements as c where a.user_id = c.user_id and c.level_of_clearence = "CLR" group by c.user_id'
        countOfUnClearedStatement = 'select count(*) from placements as c where a.user_id = c.user_id and c.level_of_clearence <> "CLR" group by c.user_id'
        lOCStatement = 'CASE WHEN a.level_of_clearence = "CLR" THEN "Placed" ELSE a.level_of_clearence END'
        HiringStatement = 'select CASE WHEN b.campus_hiring THEN "On-Campus" ELSE "Off-Campus" END from company as b where b.name = a.company_name limit 1'

        statement = f'select a.user_id,u.branch,u.email,a.company_name,a.package,({lOCStatement}),({countOfClearedStatement}),({countOfUnClearedStatement}),u.PassedOut,({HiringStatement}) as Hiring from placements as a inner join userdetails as u on a.user_id = u.userId order by a.user_id ASC;'
       
        # print(statement)
        mycursor.execute(statement)
        data = mycursor.fetchall()
        data = tuple(data)
        return render_template('crtStatistics.html',data = data)
    return redirect('/')

@app.route('/Faculty/Filters',methods =["GET", "POST"])
def applyFilters():
    if session.get("faculty") is not None:
        mydb,mycursor = connectdatabase()

        userId = request.form.get("userId")
        branch = request.form.get("branch")
        company = request.form.get("company")
        package = request.form.get("package")
        level_of_clearance = request.form.get("LOC")
        placedCount = request.form.get("placedCount")
        unplacedCount = request.form.get("unplacedCount")
        #yop = request.form.get("yop")
        condition = 'where  1 = 1'
        # print(userId)
        if(userId != ""):
            condition += f' and user = "{userId}"'
        if(branch != ""):
            condition += f' and branch = "{branch}"'
        if(company != ""):
            condition += f' and company = "{company}"'
        if(package != ""):
            package = float(package)
            condition += f' and package <= {package}'
        if(level_of_clearance != ""):
            condition += f' and loc = "{level_of_clearance}"'
        if(placedCount != ""):
            placedCount= int(placedCount)
            condition += f' and placedCount = {placedCount}'
        if(unplacedCount != ""):
            unplacedCount = int(unplacedCount)
            condition += f' and unplacedCount = {unplacedCount}'
            
        countOfClearedStatement = 'select count(*) from placements as c where a.user_id = c.user_id and a.level_of_clearence = "CLR"'
        countOfUnClearedStatement = 'select count(*) from placements as c where a.user_id = c.user_id and a.level_of_clearence <> "CLR"'
        lOCStatement = 'CASE WHEN a.level_of_clearence = "CLR" THEN "Placed" ELSE a.level_of_clearence END'
        HiringStatement = 'select CASE WHEN b.campus_hiring THEN "On-Campus" ELSE "Off-Campus" END from company as b where b.name = a.company_name limit 1'

        innerStatement = f'select a.user_id as user,u.branch as branch,u.email,a.company_name as company,a.package as package,({lOCStatement}) as loc,({countOfClearedStatement}) as placedCount,({countOfUnClearedStatement}) as unplacedCount,u.PassedOut,({HiringStatement}) as Hiring from placements as a inner join userdetails as u on a.user_id = u.userId'

        outerStatement = f' select * from ({innerStatement}) as innerTab {condition}  order by user ASC;'
        # print(outerStatement)
        mycursor.execute(outerStatement)

        data = mycursor.fetchall()
        data = tuple(data)
        return render_template('crtStatistics.html',data = data)
    return redirect('/')

@app.route('/Faculty/AddCompanyPage',methods =["GET", "POST"])
def addCompanyPage():
    if session.get('faculty') is not None:
        return render_template('addCompany.html')
    return redirect('/')

@app.route('/Faculty/AddCompany',methods =["GET", "POST"])
def addCompany():
    if session.get("faculty") is not None:
        mydb,mycursor = connectdatabase()

        company = request.form.get("company")
        package = request.form.get("package")
        role = request.form.get("role")
        gpa = request.form.get("gpa")
        backlog = request.form.get("backlog")
        branches = request.form.getlist("branch")
        url = request.form.get("url")
        campus_hiring = request.form.get("campus_hiring")

        branch = ''.join(branches)
        if(gpa != ''):
            gpa = float(gpa)
        if(campus_hiring == 'OnCampus'):
            campus_hiring = True
        else:
            campus_hiring = False

        if(url == ''):
            url=" "

        Statement = f'insert into company(name,package,role,gpa,backlogs,branch,url,campus_hiring) values("{company}",{package},"{role}",{gpa},{backlog},"{branch}","{url}",{campus_hiring});'
        mycursor.execute(Statement)
        mydb.commit()

        selectStatement = f'select company_id from company where name = "{company}" and package = {package} and role = "{role}" and gpa = {gpa} and backlogs = {backlog} and branch = "{branch}" and url = "{url}" and campus_hiring= {campus_hiring};'
        mycursor.execute(selectStatement)
        compId = mycursor.fetchall()[0][0]

        return redirect(f'/Faculty/DisplayList/{compId}')
    return redirect('/')

def getDataBasedOnCompanyId(companyId):
    mydb,mycursor = connectdatabase()
    campusHiring = 'CASE WHEN campus_hiring THEN "On-Campus" ELSE "Off-Campus" END'
    selectEligibility = f'select company_id,name,package,role,gpa,backlogs,branch,url,({campusHiring})  from company where company_id = {companyId}'
    mycursor.execute(selectEligibility)
    criteria = mycursor.fetchall()[0][1:]
    
    package  = float(criteria[1])-1.5
    gpa = float(criteria[3])
    backlogs = int(criteria[4])
    branches = criteria[5]

    maxSal = f'select max(package) from placements as p where p.user_id = u.userId and p.level_of_clearence="CLR" group by p.user_id'
    selectStatement = f'select u.userId,u.name,u.email,u.branch,u.passedOut from userdetails as u where u.gpa >= {gpa} and u.backlogs <= {backlogs} and LOCATE(u.branch,"{branches}") <> 0 and ({maxSal}) < {package} order by u.branch,u.userId ASC;' 
    mycursor.execute(selectStatement)

    data = tuple(mycursor.fetchall())
    return data,criteria

@app.route('/Faculty/DisplayList/<companyId>',methods =["GET", "POST"])
def displayList(companyId):
    if session.get("faculty") is not None:
        data,criteria = getDataBasedOnCompanyId(companyId)
        return render_template('EligibleList.html',data = data,companyId = companyId,criteria=criteria)
    return redirect('/')

@app.route('/Faculty/DownloadList/<companyId>',methods =["GET", "POST"])
def downloadList(companyId):
    if session.get("faculty") is not None:
        data,criteria = getDataBasedOnCompanyId(companyId)

        headings = ("Roll No","Name","Email","Branch","Year Of Passing")

        filename = "C:/Users/SANTHOSH/Desktop/MiniProject/omnia/ExcelData.xlsx"
        workbook1 = openpyxl.load_workbook(filename)
        
        sheet1 = workbook1['Sheet1']
        sheet1.delete_rows(1,sheet1.max_row)

        sheet1.append(headings)
        for items in data:
            sheet1.append(items)

        workbook1.save(filename)

        return send_file(filename,attachment_filename='EligibilityList.xlsx',as_attachment=True)
    return redirect('/')


#Student Portal
@app.route('/stu_login.html')
def studentLogin():
    #checking wheather faculty/student is already logged in
    if session.get("user") is not None:
        return redirect('/dashboard')
    if session.get("faculty") is not None:
        return redirect("/")
    return render_template('stu_login.html')

@app.route('/stu_login.html/validate', methods =["GET", "POST"])
def studentValidate():
    if request.method == "POST":
        adminId = request.form.get("user_name")# getting input with name = user_name in HTML form 
        password = request.form.get("password")# getting input with name = password in HTML form 
        status = isValidStudent(adminId,password)
        if status=="successfull":
            session["user"] = adminId
            session.permanent = True
            return redirect("/dashboard")
        return status
    return None

@app.route('/stu_register.html', methods =["GET", "POST"])
def studentSignUp():
    return render_template('stu_register.html')

@app.route('/stu_register.html/validate', methods =["GET", "POST"])
def studentRegistration():
    if request.method == "POST":
        userId = request.form.get("user_id")# getting input with name = user_name in HTML form 
        password = request.form.get("password")# getting input with name = password in HTML form  
        codechef = request.form.get("Codechef") 
        codeforces = request.form.get("Codeforces")
        InterviewBit = request.form.get("InterviewBit")
        spoj = request.form.get("SPOJ")
        leetcode = request.form.get("Leetcode")
        email = request.form.get("email")
        phone = request.form.get("Phone")
        branch = request.form.get("branch")
        name = request.form.get("user_name")
        cgpa = request.form.get("cgpa")
        backlogs = request.form.get("backlogs")
        yop = request.form.get("yop")

        cgpa = float(cgpa)
        status = addStudent(userId,name,branch,cgpa,backlogs,yop,password,codechef,codeforces,InterviewBit,spoj,leetcode,email,phone)
        if(status == "Successfull!!!"):
            return render_template('stu_login.html')
        return status

@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user",None)
    if "faculty" in session:
        session.pop("faculty",None)
    return redirect('/')

@app.route('/changePassword.html',methods =["GET", "POST"])
def changePasswordPage():
    if session.get("user") is not None:
        return render_template('/changePassword.html')
    return redirect("/")

@app.route('/changePassword.html/validate', methods =["GET", "POST"])
def changePasswordValidate():
    if request.method == "POST" and session.get("user") is not None:
        userId = session.get("user")# getting input with name = password in HTML form 
        oldPassword = request.form.get("oldPassword")
        status = isValidStudent(userId,oldPassword)
        if status=="successfull":
            newPassword = request.form.get("newPassword")
            updateStatus = updateStudentPassword(session.get("user"),newPassword)
            if updateStatus != "True":
                return updateStatus
        else:
            return "Sorry Wrong Password!!!"
    return redirect("/logout")

@app.route('/dashboard', methods =["GET", "POST"])
def dashboard():
    if session.get("user") is not None:
        return render_template('dashboard.html')
    return redirect('/')

@app.route('/challenges', methods =["GET", "POST"])
#tagline contains array of categoryName,taglinesForCategory, link for background Image
def dsaTracker():
    if session.get("user") is not None:
        tagline = [["Array","Harder than they seem","https://www.booleanworld.com/wp-content/uploads/2019/11/c-arrays-cover.png"],["Matrix","Tables and Logs","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSruFwK2aAnh9R9n1F5cRe9lDV6bKPt4tdk-w&usqp=CAU"],["String","THIS IS A STRING","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCNMa1dqdHVDAlEV0nkMtx5jc5BXlmXmdF0w&usqp=CAU"],["Searching & Sorting","Best to Organize","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSmYKzfnH9ntGQZXt6iQu_yhiLTHygjeelqkg&usqp=CAU"],["LinkedList","Reverse it","data:image/jpeg;base64,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"],["Binary Trees","Invert it","data:image/png;base64,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"],["Binary Search Tree","Im sorted, maybe not","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuxHUd9tr8e34lAVqoRTqNd6I8DGyOWzIMLQ&usqp=CAU"],["Greedy","Not too greedy","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTIWYHDBUbI1QYC4zRID8f_nLr5XGbdQ4fKRQ&usqp=CAU"],["Stacks & Queues","PUSH and POP thats it","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjvdnyeEiPh4-qyeb6IWP7tihuic1sLsm-vg&usqp=CAU"],["Graph","Easier than they seem","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTW1hZhGH_Dm2IJJVhL8Bs4t_xdnlCivpkM9w&usqp=CAU"],["Dynamic Programming","Everyone hates it","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRn1NuBgwrX3_6eI-83di7dqJepE9Vx1GMCNQ&usqp=CAU"],["Bit Manipulation","1 and 0","https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlkRBlCwjKA0q-0ynCm46333Ryo0iDP02Rew&usqp=CAU"]];
        return render_template('dsaTracker.html',tagline=tagline)
    return redirect('/')

@app.route('/challenges/<category>',methods=['GET','POST'])
def challangesPage(category):
        mydb,mycursor = connectdatabase()
        statement = f'SELECT * FROM dsa where topic LIKE "{category}"'
        mycursor.execute(statement)
        data = mycursor.fetchall()
        return render_template('challenges.html',data=data,category=category)

@app.route('/MyPerformance/<userId>',methods =["GET", "POST"])
def myPerformance(userId):
    uid = "18R21A1290"#default userId
    if session.get("user") is not None:
        uid = session["user"]
    elif session.get("faculty") is not None:
        uid = userId
    else:
        return redirect('/')
    mydb,mycursor = connectdatabase()
    #submission verdict details
    mycursor.execute("SELECT `Accepted`,`WrongAnswer`,`TimeLimitExceed`,`CompilationError`,`RunTimeError` FROM usersubmissions WHERE userId LIKE  %s",[uid])
    data = mycursor.fetchall()
    values = list(data)
    #contest participation details
    mycursor.execute('SELECT b.ContestTimeStamp FROM usercontestdetails as a inner join contestdetails as b on a.contestId=b.contestId where a.userid LIKE %s and a.platform="codeforces"',[uid])
    lab = mycursor.fetchall()

    mycursor.execute('SELECT a.newRating FROM usercontestdetails as a inner join contestdetails as b on a.contestId=b.contestId where a.userid LIKE %s and a.platform="codeforces"',[uid])
    val = mycursor.fetchall()

    mycursor.execute('SELECT codechefHandle, codeforcesHandle, interviewbitHandle, spojHandle, leetCodeHandle FROM userdetails where userid LIKE %s',[uid])
    handles = mycursor.fetchall()[0]
    #-------------
    labels = ["Accepted","WrongAnswer","TimeLimitExceed","CompilationError","RunTimeError"]

    selectStatement = f'SELECT * FROM leaderboardtable WHERE userId LIKE "{uid}" and scoredDate="{currentDate}"'
    mycursor.execute(selectStatement)
    leader = mycursor.fetchall()
    tags = ["binarySearch","binaryTree","matrices","arrays","probabilities","implementation","math","backtracking","numberTheory","divideAndConquer","bruteforce","dp","graphs","trees","dfs","bfs","bitManipulation","strings","dataStructures","games","greedy","hashing","sorting","twopointers","Others"]
    problemsSolved = []

    for tag in tags:
        selectStatement = f'SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE "{uid}" and b.verdict="ACCEPTED" and b.{tag}=true'
        mycursor.execute(selectStatement)
        currProblems = mycursor.fetchall()
        problemsSolved.append(currProblems)
        
    return render_template("userPerformance.html", handles = handles[2:],labels = labels, values = values, val=val, lab = lab, leader=leader, uid=uid,tags=tags, problemsSolved=problemsSolved)

@app.route('/leaderboard',methods =["GET", "POST"])
def table():
    if session.get("user") is not None:
        mydb,mycursor = connectdatabase()
        statement = f'select userId,codechef,codeforces,interviewbit,spoj,leetcode,overallScore from leaderboardtable where ScoredDate="{currentDate}" order by overallScore desc '
        mycursor.execute(statement)
        data = mycursor.fetchall()
        data = tuple(data)
        headings = ("Roll No.","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")
        return render_template('leaderboard.html',headings=headings,data=data)
    return redirect('/')

@app.route('/ActiveContests', methods =["GET", "POST"])
def currentActiveContest():
    ActiveContestsList = getActiveContests()
    platforms = ["hackerrank.com","codechef.com","codeforces.com","hackerearth.com","leetcode.com","spoj.com"]
    return render_template("activeContests.html",platforms=platforms,contestList = ActiveContestsList)

@app.route('/profile')
def studentProfile():
    if session.get("user") is not None:
        uid  = session.get("user")
        mydb,mycursor = connectdatabase()
        statement = f'select * from userdetails where userId="{uid}"'
        mycursor.execute(statement)
        data = mycursor.fetchall()
        data = list(data)
        
        scores_statement = f'select * from leaderboardtable where userId="{uid}" and scoredDate="{currentDate}"'
        mycursor.execute(scores_statement)
        scores = mycursor.fetchall()
        scores = list(scores)

        placement_statement = f'select company_name,level_of_clearence,package,exp from placements where user_id="{uid}"'
        mycursor.execute(placement_statement)
        placements = mycursor.fetchall()
        placements = list(placements)

        headings = ["Company","Level","CTC","Experience"]

        # print(placements)        
        return render_template('student_profile.html',data = data,scores = scores,headings = headings,placements = placements)
    return redirect('/')

@app.route('/eligibleCompanies')
def studentEligibleCompanies():
    if session.get("user") is not None:
        uid = session.get("user")
        mydb,mycursor = connectdatabase()
        statement = f'select * from userdetails where userId="{uid}"'
        mycursor.execute(statement)
        data = mycursor.fetchall()
        data = list(data)
        
        statement = f'select max(package) from placements where "{uid}"=user_id and level_of_clearence="CLR"'
        mycursor.execute(statement)
        package_statement = mycursor.fetchall()
        package_statement = list(package_statement)[0]
        package = package_statement[0]-1.5

        statement = f'select name,package,role,campus_hiring,url from company where company.package>={package} and {data[0][2]}>=company.gpa and {data[0][3]}<=company.backlogs and locate("{data[0][4]}",company.branch)>0'
        mycursor.execute(statement)
        companies = mycursor.fetchall()
        companies = list(companies)

        return render_template('student_companies.html',companies=companies)
    return redirect('/')

@app.route('/companyStatusForm/<companyName>')
def companyStatusForm(companyName):
    if session.get("user") is not None:
        return render_template('company_status.html',companyName=companyName)
    return redirect('/')

@app.route('/updateCompanyStatus',methods=['POST'])
def updateCompanyStatus():
    if session.get("user") is not None:
        if request.method == "POST":
            company = request.form.get("company")
            ctc = request.form.get("ctc")
            level = request.form.get("level")
            exp = request.form.get("exp")
            uid = session.get("user")
            try:
                mydb,mycursor = connectdatabase()
                statement = f'insert into placements values("{uid}","{company}","{level}",{ctc},"{exp}")'
                # print(statement)
                mycursor.execute(statement)
                mydb.commit()
            except:
                print("ERROR")
                return redirect('/profile')
        return redirect('/profile')
    return redirect('/')

@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if request.method == "POST":
        email = request.form.get("email")
        if isValidStudentEmail(email):
            statement = f'select userId from userdetails where email="{email}"'
            mydb,mycursor = connectdatabase()
            mycursor.execute(statement)
            myresult = mycursor.fetchall()
            s = Serializer(app.config['hello'],1800)
            token = s.dumps({'user_id':myresult[0][0]}).decode('utf-8')
            msg = Message('Password Reset Request',sender='noreply@demo.com',recipients=[email])
            msg.body = f'''To reset your password, visit the link:
            {url_for('reset_password',token=token,_external=True)}

                 If you did not make this request, plz ignore

            '''
            mail.send(msg)
        else:
            return "email Not Valid"
    return redirect('/')

@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_password(token):
    s = Serializer(app.config['hello'])
    try:
        user_id = s.loads(token)['user_id']
        return render_template('reset.html',token=token)
    except:
        return None

@app.route('/restPasswordUpdate/<token>',methods=['GET','POST'])
def resetPassword(token):
    if request.method == "POST":
        try:
            s = Serializer(app.config['hello'])
            user_id = s.loads(token)['user_id']
            newPassword = request.form.get("password")
            status = updateStudentPassword(user_id,newPassword)
            if not status:
                return status
            return redirect('/')
        except:
            return "Error"
    return "error"

@app.route('/forgot.html')
def forgot_page():
    return render_template('forgot.html')

def updateLeaderBoard():
    while(True):
        updateScore()
        time.sleep(24*60*60)

def updatePlatformDetails():
    while(True):
        updateCodeforcesProblems_Contests()
        time.sleep(7*24*60*60)


if __name__ == "__main__":
    leaderBoardUpdationThread = threading.Thread(target=updateLeaderBoard)
    leaderBoardUpdationThread.start()
    platformDetailsUpdationThread = threading.Thread(target=updatePlatformDetails)
    platformDetailsUpdationThread.start()
    app.run(debug=True,host="0.0.0.0")