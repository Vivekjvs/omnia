from flask import Flask,request,redirect
from MainDatabase import *
from flask.templating import render_template
app = Flask(__name__)

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
    return None

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/leaderboard')
def table():
    mydb,mycursor = connectdatabase()
    statement = "select * from leaderboardtable order by overallScore desc"
    mycursor.execute(statement)
    data = mycursor.fetchall()
    data = tuple(data)
    headings = ("Roll No.","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")

    print(data)
    return render_template('leaderboard.html',headings=headings,data=data)

@app.route('/adminLeaderboard')
def admintable():
    mydb,mycursor = connectdatabase()
    statement = "select a.userId,b.phone,b.email,a.codechef,a.codeforces,a.interviewbit,a.spoj,a.leetcode,a.overallScore from leaderboardtable as a inner join userdetails as b on a.userId = b.userId order by a.overallScore desc"
    mycursor.execute(statement)
    data = mycursor.fetchall()
    data = tuple(data)
    headings = ("Roll No.","Phone","email","CodeChef","CodeForces","InterviewBit","Spoj","LeetCode","Total Score")

    print(data)
    return render_template('admin_leaderboard.html',headings=headings,data=data)

@app.route('/stu_register.html')
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

if __name__ == "__main__":
    app.run(debug=True)