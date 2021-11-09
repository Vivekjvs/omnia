from flask import Flask,request
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

       return isValidAdmin(adminId,password)

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

       return isValidStudent(adminId,password)

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
       codechef = request.form.get("codechef")
       # getting input with name = email  in HTML form 
       codeforces = request.form.get("codeforces") 

       return addStudent(adminId,password,codechef,codeforces)


if __name__ == "__main__":
    app.run(debug=True)