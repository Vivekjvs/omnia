from os import curdir
from flask import Flask,request,redirect
from MainDatabase import *
from flask.templating import render_template
import threading,time
from scores import updateScore
from datetime import date
from codeforcesProblems_ContestDetails import updateCodeforcesProblems_Contests
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


        mycursor.execute(finalStatement)
        data = mycursor.fetchall()
        data = tuple(data)

        return render_template('admin_leaderboard.html',headings=headings,data=data,filterStatus=False)

@app.route('/MyPerformance',methods =["GET", "POST"])
def myPerformance():
    
    uid = "18r21a1290"
    mydb,mycursor = connectdatabase()
    mycursor.execute("SELECT `Accepted`,`WrongAnswer`,`TimeLimitExceed`,`CompilationError`,`RunTimeError` FROM usersubmissions WHERE userId LIKE  %s",[uid])
    data = mycursor.fetchall()
    values = list(data)
    
    mycursor.execute('SELECT b.ContestTimeStamp FROM usercontestdetails as a inner join contestdetails as b on a.contestId=b.contestId where a.userid LIKE %s and a.platform="codeforces"',[uid]);
    lab = mycursor.fetchall()

    mycursor.execute('SELECT a.newRating FROM usercontestdetails as a inner join contestdetails as b on a.contestId=b.contestId where a.userid LIKE %s and a.platform="codeforces"',[uid])
    val = mycursor.fetchall()
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

    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.binaryTree=true",[uid])
    # bt = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.matrices=true",[uid])
    # mat = mycursor.fetchall();
    
    
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.arrays=true",[uid])
    # arr = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.probabilities=true",[uid])
    # prob = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.implementation=true",[uid])
    # implementation = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.math=true",[uid])
    # math = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.backtracking=true",[uid])
    # backtracking = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.numberTheory=true",[uid])
    # number = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.divideAndConquer=true",[uid])
    # dandc = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.bruteforce=true",[uid])
    # brute = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.dp=true",[uid])
    # dp = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.graphs=true",[uid])
    # graph = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.trees=true",[uid])
    # trees = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.dfs=true",[uid])
    # dfs = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.bfs=true",[uid])
    # bfs = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.bitManipulation=true",[uid])
    # bit = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.strings=true",[uid])
    # strings = mycursor.fetchall();
    

    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.dataStructures=true",[uid])
    # ds = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.games=true",[uid])
    # games = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.greedy=true",[uid])
    # greedy = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.hashing=true",[uid])
    # hashing = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.sorting=true",[uid])
    # sorting = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.twopointers=true",[uid])
    # tp = mycursor.fetchall();
    # mycursor.execute("SELECT a.problemName,a.problemId,a.problemLink FROM problemdetails as a inner join userproblemdetails as b ON a.problemId=b.problemId WHERE b.userId LIKE %s and b.verdict='ACCEPTED' and b.Others=true",[uid])
    # others = mycursor.fetchall();
    print(problemsSolved)

    return render_template("userPerformance.html", labels = labels, values = values, val=val, lab = lab, leader=leader, uid=uid,tags=tags, problemsSolved=problemsSolved)


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

def updatePlatformDetails():
    while(True):
        updateCodeforcesProblems_Contests()
        time.sleep(7*24*60*60)
if __name__ == "__main__":
    leaderBoardUpdationThread = threading.Thread(target=updateLeaderBoard)
    leaderBoardUpdationThread.start()
    platformDetailsUpdationThread = threading.Thread(target=updatePlatformDetails)
    platformDetailsUpdationThread.start()
    app.run(debug=True)