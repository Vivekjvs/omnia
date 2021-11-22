from os import curdir
from flask import Flask,request,redirect
from MainDatabase import *
from flask.templating import render_template
import threading,time
from scores import updateScore
from datetime import date

app = Flask(__name__)
currentDate = date.today().strftime("%Y-%m-%d")

@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/fac_login.html')
def facultyLogin():
    return render_template('fac_login.html')


@app.route('/fac_login.html/validate', methods =["GET", "POST"])
def facultyValidate():
    if request.method == "POST":
        # getting input with name = user_name in HTML form 
        adminId = request.form.get("user_name")
        # getting input with name = password in HTML form 
        password = request.form.get("password")

        verdict =  isValidAdmin(adminId,password)
        print(verdict)
        if(verdict == "successfull"):
            return redirect('/adminLeaderboard')
        return verdict
    return None

@app.route('/fac_register.html', methods =["GET", "POST"])
def facultySignUp():
    return render_template('fac_register.html')

@app.route('/fac_register.html/validate', methods =["GET", "POST"])
def facultyRegistration():
    if request.method == "POST":
        # getting input with name = user_name in HTML form 
        adminId = request.form.get("user_name")
        # getting input with name = password in HTML form 
        password = request.form.get("password")
        # getting input with name = email  in HTML form 
        email = request.form.get("email") 

        return addAdmin(adminId,password,email)

@app.route('/stu_login.html')
def studentLogin():
    return render_template('stu_login.html')

@app.route('/stu_login.html/validate', methods =["GET", "POST"])
def studentValidate():
    if request.method == "POST":
        # getting input with name = user_name in HTML form 
        adminId = request.form.get("user_name")
        # getting input with name = password in HTML form 
        password = request.form.get("password")

        status = isValidStudent(adminId,password)
        if status=="successfull":
            return redirect("/dashboard")
        # return "successfull"
        return status
    return None

@app.route('/dashboard', methods =["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

@app.route('/leaderboard',methods =["GET", "POST"])
def table():
    mydb,mycursor = connectdatabase()
    statement = f'select userId,codechef,codeforces,interviewbit,spoj,leetcode,overallScore from leaderboardtable where scoredDate="{currentDate}" order by overallScore desc '
    mycursor.execute(statement)
    data = mycursor.fetchall()
    data = tuple(data)
    headings = ("Roll No.","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")

    print(data)
    return render_template('leaderboard.html',headings=headings,data=data)

@app.route('/adminLeaderboard', methods =["GET", "POST"])
def admintable():
    mydb,mycursor = connectdatabase()
    statement = f'select a.userId,b.phone,b.email,a.codechef,a.codeforces,a.interviewbit,a.spoj,a.leetcode,a.overallScore from leaderboardtable as a inner join userdetails as b on a.userId = b.userId where scoredDate="{currentDate}" order by a.overallScore desc '
    mycursor.execute(statement)
    data = mycursor.fetchall()
    data = tuple(data)
    headings = ("Roll No.","Phone","email","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")

    return render_template('admin_leaderboard.html',headings=headings,data=data,filterStatus= True)

@app.route('/adminLeaderboardFilter', methods =["GET", "POST"])
def adminFiltertable():
    mydb,mycursor = connectdatabase()
    if request.method == "POST":
        # getting input with name = user_name in HTML form 
        startDate = request.form.get("startDate")
        # getting input with name = password in HTML form 
        endDate = request.form.get("endDate")
        
        startStatement = f'select userId,codechef,codeforces,interviewbit,spoj,leetcode,overallScore from leaderboardtable where scoredDate="{startDate}"'

        endStatement = f'select userId,codechef,codeforces,interviewbit,spoj,leetcode,overallScore from leaderboardtable where scoredDate="{endDate}"'
        
        currentStatement = f'select a.userid as userId,b.codechef-a.codechef as codechef,b.codeforces-a.codeforces as codeforces, b.interviewbit-a.interviewbit as interviewbit, b.spoj-a.spoj as spoj, b.leetcode-a.leetcode as leetcode, b.overallScore-a.overallScore as overallScore from ({startStatement}) as a,({endStatement}) as b where a.userId=b.userId'

        finalStatement = f'select c.userId,d.phone,d.email,c.codechef,c.codeforces,c.interviewbit,c.spoj,c.leetcode,c.overallScore from ({currentStatement}) as c inner join userdetails as d on c.userId = d.userId order by c.overallScore desc '
        
        headings = ("Roll No.","Phone","email","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")

        print(finalStatement)
        mycursor.execute(finalStatement)
        data = mycursor.fetchall()
        data = tuple(data)

        return render_template('admin_leaderboard.html',headings=headings,data=data,filterStatus=False)


@app.route('/stu_register.html', methods =["GET", "POST"])
def studentSignUp():
    return render_template('stu_register.html')

@app.route('/stu_register.html/validate', methods =["GET", "POST"])
def studentRegistration():
    if request.method == "POST":
        # getting input with name = user_name in HTML form 
        adminId = request.form.get("user_name")
        # getting input with name = password in HTML form 
        password = request.form.get("password")
        # getting input with name = email  in HTML form 
        codechef = request.form.get("Codechef")
        # getting input with name = email  in HTML form 
        codeforces = request.form.get("Codeforces") 

        InterviewBit = request.form.get("InterviewBit")
        spoj = request.form.get("SPOJ")
        leetcode = request.form.get("Leetcode")
        email = request.form.get("email")
        phone = request.form.get("Phone")

        status = addStudent(adminId,password,codechef,codeforces,InterviewBit,spoj,leetcode,email,phone)
        if(status == "Successfull!!!"):
            return render_template('stu_login.html')
        return status

def updateLeaderBoard():
    while(True):
        updateScore()
        time.sleep(24*60*60)

if __name__ == "__main__":
    leaderBoardUpdationThread = threading.Thread(target=updateLeaderBoard)
    leaderBoardUpdationThread.start()
    app.run(debug=True)