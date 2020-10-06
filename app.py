import os
import re
import csv

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///school3.db")


@app.route("/", methods=["GET"])
def home():
    """Show portfolio of stocks"""
    if request.method == "GET":
        return render_template("index.html") 
    #return apology("TODO")

@app.route("/contact", methods=["GET"])
def contact():
    """Show portfolio of stocks"""
    if request.method == "GET":
        return render_template("contact.html") 
    #return apology("TODO")

@app.route("/about", methods=["GET"])
def about():
    """Show portfolio of stocks"""
    if request.method == "GET":
        return render_template("about.html") 
    #return apology("TODO")

@app.route("/blog", methods=["GET"])
def blog():
    """Show portfolio of stocks"""
    if request.method == "GET":
        return render_template("blog.html") 
    #return apology("TODO")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("admin.html")
    #return apology("TODO")


@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    """Show history of transactions"""
    if request.method == "GET":
        return render_template("teachers.html")
    #return apology("TODO")

@app.route("/students", methods=["GET", "POST"])
def students():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("students.html")
    #return apology("TODO")


@app.route("/admin_login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM persons JOIN prsntype ON persons.prsntypeid = prsntype.prsntypeid WHERE username = :username AND prsntype = :admindb",
                          username=request.form.get("username"), admindb="admin")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["admin"] = rows[0]["prsnid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("admin.html")

@app.route("/teacher_login", methods=["GET", "POST"])
def teacher_login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM persons JOIN prsntype ON persons.prsntypeid = prsntype.prsntypeid WHERE username = :username AND prsntype = :teacherdb",
                          username=request.form.get("username"), teacherdb="teacher")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["teachers"] = rows[0]["prsnid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("teachers.html")



@app.route("/students_login", methods=["GET", "POST"])
def students_login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM persons JOIN prsntype ON persons.prsntypeid = prsntype.prsntypeid WHERE username = :username AND prsntype = :studentdb",
                          username=request.form.get("username"), studentdb="student")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and / or password", 403)

        # Remember which user has logged in
        session["students"] = rows[0]["prsnid"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("students.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/admin_register_admin", methods=["GET", "POST"])
@login_required
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("admin_register_admin.html")
    else:
        if not request.form.get("username"):
            return apology("must provide username", 403)

        if not  request.form.get("password"):
            return apology("must provide password", 403)
        usernamedb = db.execute("SELECT username FROM persons WHERE username = :usernamedb", usernamedb=request.form.get("username"))
        if len(usernamedb) != 1:
            pswd_hash = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO prsntype (prsntype) VALUES (:admindb)", admindb="admin")

            last_id = db.execute("SELECT MAX(prsntypeid) AS id FROM prsntype")
            db.execute("INSERT INTO persons (prsntypeid, username, hash) VALUES (?, ?, ?)", last_id[0]['id'], request.form.get("username"), pswd_hash)
            return redirect("/")
        else:
            return apology("username already taken", 403)
    #return apology("TODO")

@app.route("/admin_register_teachers", methods=["GET", "POST"])
@login_required
def admin_register_teacher():
    """Register user"""
    if request.method == "GET":
        return render_template("admin_register_teachers.html")
    else:
        if not request.form.get("name") and request.form.get("year") == "year":
            return apology("must provide Full name and year", 403)

        if request.form.get("tgender") == "gender" and request.form.get("class") == "class":
            return apology("must select gender and class", 403)

        classes = [request.form.get("js1"), request.form.get("js2"), request.form.get("js3"), request.form.get("ss1"),
                    request.form.get("ss2"), request.form.get("ss3")]
        all_class = []

        for classs in classes:
            if classs == None:
                continue
            else:
                all_class.append(classs)

        length = len(all_class)
        if len(all_class) > 3 or len(all_class) < 1:
            return apology(f"must select at least 1 class & maximum 3  {length}", 403)


        usernamedb = db.execute("SELECT username FROM persons WHERE username = :usernamedb", usernamedb=request.form.get("name"))
        if len(usernamedb) != 1:
            pswd_hash = generate_password_hash("1234")
            db.execute("INSERT INTO prsntype (prsntype) VALUES (:teacherdb)", teacherdb="teacher")

            last_id = db.execute("SELECT MAX(prsntypeid) AS id FROM prsntype")
            db.execute("INSERT INTO persons (prsntypeid, username, hash) VALUES (?, ?, ?)", last_id[0]['id'], request.form.get("name"), pswd_hash)

            last_prsnid = db.execute("SELECT MAX(prsnid) AS id FROM persons")

            db.execute("INSERT INTO teacherdata (tchr_prsnid, tchr_name, tchr_gender) VALUES (:tchr_prsniddb, :tchrdnamedb, :tchr_genderdb)", 
                        tchr_prsniddb=last_prsnid[0]['id'], tchrdnamedb=request.form.get("name"), tchr_genderdb=request.form.get("tgender"))
            db.execute("INSERT INTO year (yrname) VALUES (:yrnamedb)", yrnamedb=request.form.get("year"))

            last_yrid = db.execute("SELECT MAX(yrid) AS id FROM year")

            for x in range(len(all_class)):
                db.execute("INSERT INTO class (cls_prsnid, cls_yrid, clsname) VALUES (:cls_prsniddb, :cls_yriddb, :clsnamedb)", 
                            cls_prsniddb=last_prsnid[0]['id'], cls_yriddb=last_yrid[0]['id'], clsnamedb=all_class[x])
            return redirect("/")
        else:
            return apology("username already taken", 403)
    #return apology("TODO")

@app.route("/admin_register_students", methods=["GET", "POST"])
@login_required
def admin_register_students():
    """Register user"""
    if request.method == "GET":
        return render_template("admin_register_students.html")
    else:
        if not request.form.get("name") and request.form.get("year") == "year":
            return apology("must provide Full name and year", 403)

        if request.form.get("tgender") == "gender" and request.form.get("class") == "class":
            return apology("must select gender and class", 403)

        if not request.form.get("dob"):
            return apology("kindly choose date of birth")

        classes = [request.form.get("js1"), request.form.get("js2"), request.form.get("js3"), request.form.get("ss1"),
                    request.form.get("ss2"), request.form.get("ss3")]
        all_class = []

        for classs in classes:
            if classs == None:
                continue
            else:
                all_class.append(classs)

        if len(all_class) > 1 or len(all_class) < 1:
            return apology("must select at least 1 class", 403)


        usernamedb = db.execute("SELECT username FROM persons WHERE username = :usernamedb", usernamedb=request.form.get("name"))
        if len(usernamedb) != 1:
            pswd_hash = generate_password_hash("1234")
            db.execute("INSERT INTO prsntype (prsntype) VALUES (:studentsdb)", studentsdb="student")

            last_id = db.execute("SELECT MAX(prsntypeid) AS id FROM prsntype")
            db.execute("INSERT INTO persons (prsntypeid, username, hash) VALUES (?, ?, ?)", last_id[0]['id'], request.form.get("name"), pswd_hash)

            last_prsnid = db.execute("SELECT MAX(prsnid) AS id FROM persons")

            db.execute("INSERT INTO studentdata (std_prsnid, stdname, std_dob, std_gender) VALUES (:tchr_prsniddb, :tchrdnamedb, :std_dobdb, :tchr_genderdb)", 
                        tchr_prsniddb=last_prsnid[0]['id'], tchrdnamedb=request.form.get("name"), std_dobdb=request.form.get("dob"), tchr_genderdb=request.form.get("tgender"))
            db.execute("INSERT INTO year (yrname) VALUES (:yrnamedb)", yrnamedb=request.form.get("year"))

            last_yrid = db.execute("SELECT MAX(yrid) AS id FROM year")

            db.execute("INSERT INTO class (cls_prsnid, cls_yrid, clsname) VALUES (:cls_prsniddb, :cls_yriddb, :clsnamedb)", 
                        cls_prsniddb=last_prsnid[0]['id'], cls_yriddb=last_yrid[0]['id'], clsnamedb=all_class[0])
            return redirect("/")
        else:
            return apology("username already taken", 403)
    #return apology("TODO")


@app.route("/teachers_register_students", methods=["GET", "POST"])
@login_required
def teachers_register_students():
    """Register user"""
    if request.method == "GET":
        return render_template("teachers_register_students.html")
    else:
        if not request.form.get("name") and request.form.get("year") == "year":
            return apology("must provide Full name and year", 403)

        if request.form.get("tgender") == "gender" and request.form.get("class") == "class":
            return apology("must select gender and class", 403)

        if not request.form.get("dob"):
            return apology("kindly choose date of birth")

        classes = [request.form.get("js1"), request.form.get("js2"), request.form.get("js3"), request.form.get("ss1"),
                    request.form.get("ss2"), request.form.get("ss3")]
        all_class = []

        for classs in classes:
            if classs == None:
                continue
            else:
                all_class.append(classs)

        if len(all_class) > 1 or len(all_class) < 1:
            return apology("must select at least 1 class", 403)


        usernamedb = db.execute("SELECT username FROM persons WHERE username = :usernamedb", usernamedb=request.form.get("name"))
        if len(usernamedb) != 1:
            pswd_hash = generate_password_hash("1234")
            db.execute("INSERT INTO prsntype (prsntype) VALUES (:studentsdb)", studentsdb="student")

            last_id = db.execute("SELECT MAX(prsntypeid) AS id FROM prsntype")
            db.execute("INSERT INTO persons (prsntypeid, username, hash) VALUES (?, ?, ?)", last_id[0]['id'], request.form.get("name"), pswd_hash)

            last_prsnid = db.execute("SELECT MAX(prsnid) AS id FROM persons")

            db.execute("INSERT INTO studentdata (std_prsnid, stdname, std_dob, std_gender) VALUES (:tchr_prsniddb, :tchrdnamedb, :std_dobdb, :tchr_genderdb)", 
                        tchr_prsniddb=last_prsnid[0]['id'], tchrdnamedb=request.form.get("name"), std_dobdb=request.form.get("dob"), tchr_genderdb=request.form.get("tgender"))
            db.execute("INSERT INTO year (yrname) VALUES (:yrnamedb)", yrnamedb=request.form.get("year"))

            last_yrid = db.execute("SELECT MAX(yrid) AS id FROM year")

            db.execute("INSERT INTO class (cls_prsnid, cls_yrid, clsname) VALUES (:cls_prsniddb, :cls_yriddb, :clsnamedb)", 
                        cls_prsniddb=last_prsnid[0]['id'], cls_yriddb=last_yrid[0]['id'], clsnamedb=all_class[0])
            return redirect("/")
        else:
            return apology("username already taken", 403)
    #return apology("TODO")


@app.route("/admin_teachers", methods=["GET"])
@login_required
def admin_teachers():
    """Sell shares of stock"""

    if request.method == "GET":
        rows = db.execute("SELECT * FROM teacherdata JOIN persons ON teacherdata.tchr_prsnid = persons.prsnid JOIN prsntype ON persons.prsntypeid = prsntype.prsntypeid JOIN class ON class.cls_prsnid = persons.prsnid JOIN year ON class.cls_yrid = year.yrid WHERE prsntype.prsntype = :teacherdb AND year.yrname = :yrnamedb",
                    teacherdb="teacher", yrnamedb=2016)
        tchr_name = []
        tchr_gender = []
        tchr_class = []
        tchr_yr = []

        for name in rows:
            tchr_name.append(name['tchr_name'])
        for gender in rows:
            tchr_gender.append(gender['tchr_gender'].upper())
        for classs in rows:
            tchr_class.append(classs['clsname'].upper())
        for year in rows:
            tchr_yr.append(year['yrname'])

        total = len(tchr_name)

        return render_template("admin_teachers.html", names=tchr_name, gender=tchr_gender, classs=tchr_class, year=tchr_yr, allname=total)

    #return apology("TODO")

@app.route("/admin_students", methods=["GET"])
@login_required
def admin_students():
    """Sell shares of stock"""
    if request.method == "GET":
        rows = db.execute("SELECT * FROM studentdata JOIN persons ON studentdata.std_prsnid = persons.prsnid JOIN prsntype ON persons.prsntypeid = prsntype.prsntypeid JOIN class ON class.cls_prsnid = persons.prsnid JOIN year ON class.cls_yrid = year.yrid WHERE prsntype.prsntype = :studentdb",
                    studentdb="student")
        std_name = []
        std_gender = []
        std_dob = []
        std_class = []
        std_yr = []

        for name in rows:
            std_name.append(name['stdname'])
        for gender in rows:
            std_gender.append(gender['std_gender'].upper())
        for dob in rows:
            std_dob.append(dob['std_dob'])
        for classs in rows:
            std_class.append(classs['clsname'].upper())
        for year in rows:
            std_yr.append(year['yrname'])

        total = len(std_name)

        return render_template("admin_students.html", names=std_name, dob=std_dob, gender=std_gender, classs=std_class, year=std_yr, allname=total)


    #return apology("TODO")

@app.route("/teachers_students", methods=["GET"])
@login_required
def teachers_students():
    """Sell shares of stock"""
    if request.method == "GET":

        tchr_class = db.execute("SELECT clsname FROM class WHERE cls_prsnid = :teacherdb",
            teacherdb=session['teachers'])
        tchr_ls = []

        for each in tchr_class:
            tchr_ls.append(each['clsname'])

        std_name = []
        std_gender = []
        std_dob = []
        std_class = []
        std_yr = []

        for clss in tchr_ls:
            rows = db.execute("SELECT * FROM studentdata JOIN persons ON studentdata.std_prsnid = persons.prsnid JOIN prsntype ON persons.prsntypeid = prsntype.prsntypeid JOIN class ON class.cls_prsnid = persons.prsnid JOIN year ON class.cls_yrid = year.yrid WHERE prsntype.prsntype = :studentdb AND class.clsname = :clssdb",
                        studentdb="student", clssdb=clss)
            for name in rows:
                std_name.append(name['stdname'])
            for gender in rows:
                std_gender.append(gender['std_gender'].upper())
            for dob in rows:
                std_dob.append(dob['std_dob'])
            for classs in rows:
                std_class.append(classs['clsname'].upper())
            for year in rows:
                std_yr.append(year['yrname'])

        total = len(std_name)

        return render_template("teachers_students.html", names=std_name, dob=std_dob, gender=std_gender, classs=std_class, year=std_yr, allname=total)


    #return apology("TODO")


@app.route("/admin_result_upload", methods=["GET", "POST"])
@login_required
def admin_result_upload():
    """Sell shares of stock"""

    if request.method == "GET":
        return render_template("admin_result_upload.html")
    else:
        stdname = request.form.get("name")
        term = request.form.get("term")
        year = request.form.get("year")
        result_file = request.form.get("result")

        classes = [request.form.get("js1"), request.form.get("js2"), request.form.get("js3"), request.form.get("ss1"),
                    request.form.get("ss2"), request.form.get("ss3")]
        all_class = []
        binaryfile = []

        for classs in classes:
            if classs == None:
                continue
            else:
                all_class.append(classs)

        if len(all_class) < 1:
            return apology("must select at least 1 class", 403)
        if not term or not year or not result_file or not stdname:
            return apology("sorry all field must filled", 403)

        student_recordn = db.execute("SELECT stdname FROM studentdata WHERE stdname = :studentdb", studentdb=stdname)
        student_recordc = db.execute("SELECT clsname FROM class JOIN studentdata ON class.cls_prsnid = studentdata.std_prsnid WHERE stdname = :studentdb", studentdb=stdname)
        student_recordr = db.execute("SELECT stdresult FROM result JOIN studentdata ON result.rst_stdid = studentdata.stdid JOIN terms ON result.rst_trmid = terms.trmid JOIN year ON result.rst_yrid = year.yrid JOIN class ON result.rst_clsid = class.clsid WHERE stdname = :studentdb AND terms.trmname = :termdb AND year.yrname = :yrnamedb AND class.clsname = :classdb",
                                        studentdb=stdname, termdb=term, yrnamedb=year, classdb=all_class[0])

        if len(student_recordn) != 1:
            return apology("make sure all field data is valid", 403)
        if len(student_recordc) < 1:
            return apology("make sure std is in class", 403)
        if len(student_recordr) > 0:
            return apology("make sure result hasn't been uploaded", 403)

        if not re.search(".pdf$", result_file):
            return apology("make sure it is a valid pdf", 403)

        try:
                with open(result_file, "rb") as fileb:
                        binarydata = fileb.read()
                        binaryfile.append(binarydata)

        except FileNotFoundError:
                return apology("file not found", 403)

        db.execute("INSERT INTO terms (trmname) VALUES (?)", term)
        term_info = db.execute("SELECT MAX(trmid) FROM terms")
        student_info = db.execute("SELECT * FROM class JOIN studentdata ON class.cls_prsnid = studentdata.std_prsnid JOIN year ON class.cls_yrid = year.yrid WHERE stdname = :studentdb AND yrname = :yrnamedb AND clsname = :clsnamedb",
                    studentdb=stdname, yrnamedb=year, clsnamedb=all_class[0])
        clsid = student_info[0]['clsid']
        yrid = student_info[0]['cls_yrid']
        stdid = student_info[0]['stdid']
        trmid = term_info[0]['MAX(trmid)']

        db.execute("INSERT INTO result (rst_stdid, stdresult, rst_trmid, rst_yrid, rst_clsid) VALUES (?, ?, ?, ?, ?)",
            stdid, binaryfile[0], trmid, yrid, clsid)

        
        return redirect("/")

        #return apology("TODO")
        

@app.route("/teachers_result_upload", methods=["GET", "POST"])
@login_required
def teachers_result_upload():
    """Sell shares of stock"""

    if request.method == "GET":
        return render_template("teachers_result_upload.html")
    else:
        stdname = request.form.get("name")
        term = request.form.get("term")
        year = request.form.get("year")
        result_file = request.form.get("result")

        classes = [request.form.get("js1"), request.form.get("js2"), request.form.get("js3"), request.form.get("ss1"),
                    request.form.get("ss2"), request.form.get("ss3")]
        all_class = []
        tchr_all_class = []
        binaryfile = []

        for classs in classes:
            if classs == None:
                continue
            else:
                all_class.append(classs)

        if len(all_class) < 1:
            return apology("must select at least 1 class", 403)
        if not term or not year or not result_file or not stdname:
            return apology("sorry all field must filled", 403)

        student_recordn = db.execute("SELECT stdname FROM studentdata WHERE stdname = :studentdb", studentdb=stdname)
        student_recordc = db.execute("SELECT clsname FROM class JOIN studentdata ON class.cls_prsnid = studentdata.std_prsnid WHERE stdname = :studentdb", studentdb=stdname)
        student_recordr = db.execute("SELECT stdresult FROM result JOIN studentdata ON result.rst_stdid = studentdata.stdid JOIN terms ON result.rst_trmid = terms.trmid JOIN year ON result.rst_yrid = year.yrid JOIN class ON result.rst_clsid = class.clsid WHERE stdname = :studentdb AND terms.trmname = :termdb AND year.yrname = :yrnamedb AND class.clsname = :classdb",
                                        studentdb=stdname, termdb=term, yrnamedb=year, classdb=all_class[0])
        teacher_class = db.execute("SELECT clsname FROM class JOIN year ON class.cls_yrid = year.yrid WHERE class.cls_prsnid = :tchriddb AND year.yrname = :yeardb",
            tchriddb=session['teachers'], yeardb=year)
        

        for classs in teacher_class:
            tchr_all_class.append(classs['clsname'])

        if len(student_recordn) != 1:
            return apology("make sure all field data is valid", 403)
        if len(student_recordc) < 1:
            return apology("make sure std is in class", 403)
        if len(student_recordr) > 0:
            return apology("make sure result hasn't been uploaded", 403)
        if all_class[0] not in tchr_all_class:
            return apology("sorry you can't upload result for this class", 403)

        if not re.search(".pdf$", result_file):
            return apology("make sure it is a valid pdf", 403)

        try:
                with open(f"static/upload/Student_result/2016/First/{result_file}", "rb") as fileb:
                        binarydata = fileb.read()
                        binaryfile.append(binarydata)

        except FileNotFoundError:
                return apology("file not found", 403)   
                
        db.execute("INSERT INTO terms (trmname) VALUES (?)", term)
        term_info = db.execute("SELECT MAX(trmid) FROM terms")
        student_info = db.execute("SELECT * FROM class JOIN studentdata ON class.cls_prsnid = studentdata.std_prsnid JOIN year ON class.cls_yrid = year.yrid WHERE stdname = :studentdb AND yrname = :yrnamedb AND clsname = :clsnamedb",
                    studentdb=stdname, yrnamedb=year, clsnamedb=all_class[0])
        clsid = student_info[0]['clsid']
        yrid = student_info[0]['cls_yrid']
        stdid = student_info[0]['stdid']
        trmid = term_info[0]['MAX(trmid)']

        db.execute("INSERT INTO result (rst_stdid, stdresult, rst_trmid, rst_yrid, rst_clsid) VALUES (?, ?, ?, ?, ?)",
            stdid, binaryfile[0], trmid, yrid, clsid)

        
        return redirect("/")

        #return apology("TODO")
    

@app.route("/students_check_result", methods=["GET", "POST"])
@login_required
def students_check_result():
    """Sell shares of stock"""

    if request.method == "GET":
        student_class_ls = db.execute("SELECT clsname FROM class WHERE cls_prsnid = :studendb", studendb=session['students'])
        return render_template("students_check_result.html", student_class_ls=student_class_ls)
    else:
        stdpass = request.form.get("password")
        term = request.form.get("term")
        year = request.form.get("year")
        student_class = request.form.get("class")

        if student_class == "class":
            return apology("sorry you must select a class", 403)

        rows = db.execute("SELECT * FROM persons WHERE persons.prsnid = :owner", owner=session['students'])
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], stdpass):
            return apology("invalid password", 403)

        #binaryfile = ("SELECT stdresult FROM result JOIN studentdata ON stdresult.rst_stdid = studentdata.stdid JOIN terms ON stdresult.rst_trmid = terms.trmid JOIN year ON stdresult.rst_yrid = year.yrid JOIN class ON stdresult.rst_clsid = class.clsid WHERE studentdata.std_prsnid = :studentdb AND terms.trmname = :termdb AND year.yrname = :yrnamedb AND class.clsname = :clsnamedb",
                       #studentdb=, termdb=, yrnamedb=, clsnamedb=)

        student_result = db.execute("SELECT stdresult FROM result JOIN studentdata ON result.rst_stdid = studentdata.stdid JOIN terms ON result.rst_trmid = terms.trmid JOIN year ON result.rst_yrid = year.yrid JOIN class ON result.rst_clsid = class.clsid WHERE std_prsnid = :studentdb AND terms.trmname = :termdb AND year.yrname = :yrnamedb AND class.clsname = :classdb",
                                        studentdb=session['students'], termdb=term, yrnamedb=year, classdb=student_class)

        if len(student_result) > 1:
            return apology("sorry there is a problem fetching result", 403)
        if len(student_result) < 1:
            return apology("No result found", 403)
        if len(student_result) == None:
            return apology("result not yet uploaded", 403)

        #if not re.search(".pdf$", result_file):
            #return apology("make sure it is a valid pdf", 403)

        result_file = student_result[0]['stdresult']

        with open("static/result/result.pdf", "wb") as file:
            result_in_pdf = file.write(result_file)

        #with open("result.pdf", "r") as fileb:
            #binarydata = fileb.read()


            return redirect("static/result/result.pdf")


    #return apology("TODO")



@app.route("/students_change_password", methods=["GET", "POST"])
@login_required
def students_change_password():
    """Sell shares of stock"""

    if request.method == "GET":
        return render_template("students_change_password.html")
    else:

        old = request.form.get("old")
        new1 = request.form.get("new1")
        new2 = request.form.get("new2")

        if not old or not new1 or not new2:
            return apology("All field must be validated", 403)
        rows = db.execute("SELECT hash FROM persons WHERE prsnid = :owner", owner=session["students"])

        if not check_password_hash(rows[0]["hash"], old):
            return apology("Old password invalid!", 403)
        else:
            if new1 == new2:
                db.execute("UPDATE persons SET hash = :new_passdb WHERE prsnid = :owner", new_passdb=generate_password_hash(new2), owner=session["students"])
                return redirect("/")
            else:
                return apology("Confirm Password", 403)

    #return apology("TODO")


@app.route("/admin_import_teachers", methods=["GET", "POST"])
@login_required
def admin_import_teachers():
    """Sell shares of stock"""

    if request.method == "GET":
        return render_template("admin_import_teachers.html")
    else:
        csv_file = request.form.get("csv_file")

        if not re.search(".csv$", csv_file):
            return apology("sorry not a csv file", 403)

        ls_name = []
        ls_genders = []
        ls_year = []
        ls_classs = []
        try:
            with open(csv_file, "r") as csv_f:
                details = csv.reader(csv_f)

                if details == "":
                    return apology("sorry you must fill in correct data in the csv", 403)

                for row in details:
                    name = row[0]
                    gender = row[1]
                    year = row[2]
                    classs = row[3]

                    ls_class = ["js1", "js2", "js3", "ss1", "ss2", "ss3", "class"]
                    ls_gender = ["f", "m", "gender"]

                    if name == "":
                        return apology("csv file not properly filled", 403)
                    if gender not in ls_gender:
                        return apology("csv file not properly filled (gender)", 403)

                    if year != "year":
                        csv_year = year
                        year_format = "%Y"
                        try:
                            datetime.strptime(csv_year, year_format)
                        except ValueError:
                            return apology("Year format not properly filled (YYYY)", 403)

                    ls_classs.append(classs)
                    for classes in range(len(ls_classs)):
                        each_classs = ls_classs[classes].split()
                        for one_class in each_classs:
                            if one_class not in ls_class:
                                return apology(f"csv file not properly filled (class) {one_class}", 403)

                    # Append teachers' name, gender, year
                    if name != "name" and gender != "gender" and year != "year":
                        ls_name.append(name)
                        ls_genders.append(gender)
                        ls_year.append(year)

                for usr in range(len(ls_name)):
                    #Start identation from here 

                    usernamedb = db.execute("SELECT username FROM persons WHERE username = :usernamedb", usernamedb=ls_name[usr])

                    if len(usernamedb) != 0:
                        return apology("username already taken", 403)
                        ########################################################

                for items in range(len(ls_name)):
                        pswd_hash = generate_password_hash("1234")

                        db.execute("INSERT INTO prsntype (prsntype) VALUES (:teacherdb)", teacherdb="teacher")

                        last_id = db.execute("SELECT MAX(prsntypeid) AS id FROM prsntype")

                        db.execute("INSERT INTO persons (prsntypeid, username, hash) VALUES (?, ?, ?)", last_id[0]['id'], ls_name[items], pswd_hash)

                        last_prsnid = db.execute("SELECT MAX(prsnid) AS id FROM persons")

                        db.execute("INSERT INTO teacherdata (tchr_prsnid, tchr_name, tchr_gender) VALUES (:tchr_prsniddb, :tchrdnamedb, :tchr_genderdb)", 
                                    tchr_prsniddb=last_prsnid[0]['id'], tchrdnamedb=ls_name[items], tchr_genderdb=ls_genders[items])

                        db.execute("INSERT INTO year (yrname) VALUES (:yrnamedb)", yrnamedb=ls_year[items])

                        last_yrid = db.execute("SELECT MAX(yrid) AS id FROM year")

                        #if len(classs) != 0:
                            #if len(classs) > 2:
                                #TODO FOR 3 CLASSES

                        classes = ls_classs[items +1].split() #Skip the class string

                        for each in classes:
                            db.execute("INSERT INTO class (cls_prsnid, cls_yrid, clsname) VALUES (:cls_prsniddb, :cls_yriddb, :clsnamedb)", 
                                    cls_prsniddb=last_prsnid[0]['id'], cls_yriddb=last_yrid[0]['id'], clsnamedb=each)
                        
                            #else:
                                #TODO FOR 2 CLASSES
                        #else:
                            #TODO FOR 1 CLASS remember to skip the first row which is the header of the csv
                            #return apoloogy("class field must not be empty", 403)
                return redirect("/")
        except FileNotFoundError:
            return apology("csv not readable or not found", 403)


        # Fetch each teacher deails in file 
                
        #return redirect("/")
        #return apology("TODO")


@app.route("/admin_import_students", methods=["GET", "POST"])
@login_required
def admin_import_students():
    """Sell shares of stock"""
    if request.method == "GET":
        return render_template("admin_import_students.html")
    else:

        form_classs = request.form.get("class")

        if form_classs == "class":
            return apology("Sorry you must select students class", 403)

        csv_file = request.form.get("csv_file")

        if not re.search(".csv$", csv_file):
            return apology("sorry not a csv file", 403)

        try:
            with open(csv_file, "r") as csv_f:
                details = csv.reader(csv_f)

                if details == "":
                    return apology("sorry you must fill in correct data in the csv")

                ls_name = []
                ls_genders = []
                ls_year = []
                ls_birth = []
                ls_classs = []
                    

                for row in details:
                    name = row[0]
                    gender = row[1]
                    year = row[2]
                    birth = row[3]
                    classs = row[4]

                    #all_classes = [ class1 = for each_class in classs ]
                    ls_gender = ["f", "m", "gender"]
                    ls_class = ["js1", "js2", "js3", "ss1", "ss2", "ss3", "class"]

                    if name == "" or len(name) > 64:
                        return apology("csv file not properly filled", 403)
                    if gender not in ls_gender:
                        return apology("csv file not properly filled (gender)", 403)
                        
                    if year != "year":
                        csv_year = year
                        year_format = "%Y"
                        try:
                            datetime.strptime(csv_year, year_format)
                        except ValueError:
                            return apology("Year fromat not properly filled (YYYY)", 403)
                            

                    if birth != "birth":
                        csv_birth = birth
                        birth_format = "%d/%m/%Y" #Date format DD/MM/YYYY
                        try:
                            datetime.strptime(csv_birth, birth_format)
                        except ValueError:
                            return apology("Birth fromat not properly filled (DD/MM/YYYY)", 403)
                            


                    # Remember to put a drop down in the submission page csv_class=form_class
                    if classs != "class":
                        if classs != form_classs:
                            return apology("Class not properly filled")
                        


                    if name != "name" and gender != "gender" and year != "year" and birth != "birth" and classs != "class":
                        ls_name.append(name)
                        ls_genders.append(gender)
                        ls_year.append(year)
                        ls_birth.append(birth)
                        ls_classs.append(classs)

                for usr in range(len(ls_name)):
                    #Start identation from here 

                    usernamedb = db.execute("SELECT username FROM persons WHERE username = :usernamedb", usernamedb=ls_name[usr])

                    if len(usernamedb) != 0:
                        return apology("username already taken", 403)
                        ########################################################
                        
                for items in range(len(ls_name)):
                    # Use student name to check if their name exist
                    #print(ls_name[each])
                    #print(ls_genders[each])
                    #print(ls_year[each])
                    #print(ls_birth[each])
                    #print(ls_classs[each])
                    
                    pswd_hash = generate_password_hash("1234")

                    db.execute("INSERT INTO prsntype (prsntype) VALUES (:teacherdb)", teacherdb="student")

                    last_id = db.execute("SELECT MAX(prsntypeid) AS id FROM prsntype")

                    db.execute("INSERT INTO persons (prsntypeid, username, hash) VALUES (?, ?, ?)", last_id[0]['id'], ls_name[items], pswd_hash)

                    last_prsnid = db.execute("SELECT MAX(prsnid) AS id FROM persons")

                    db.execute("INSERT INTO studentdata (std_prsnid, stdname, std_dob, std_gender) VALUES (:tchr_prsniddb, :tchrdnamedb, :std_dobdb, :tchr_genderdb)", 
                                tchr_prsniddb=last_prsnid[0]['id'], tchrdnamedb=ls_name[items], std_dobdb=ls_birth[items], tchr_genderdb=ls_genders[items])

                    db.execute("INSERT INTO year (yrname) VALUES (:yrnamedb)", yrnamedb=ls_year[items])

                    last_yrid = db.execute("SELECT MAX(yrid) AS id FROM year")

                    #if len(classs) != 0:
                        #if len(classs) > 2:
                            #TODO FOR 3 CLASSES

                    db.execute("INSERT INTO class (cls_prsnid, cls_yrid, clsname) VALUES (:cls_prsniddb, :cls_yriddb, :clsnamedb)", 
                            cls_prsniddb=last_prsnid[0]['id'], cls_yriddb=last_yrid[0]['id'], clsnamedb=ls_classs[items])
                    
                        #else:
                            #TODO FOR 2 CLASSES
                    #else:
                        #TODO FOR 1 CLASS remember to skip the first row which is the header of the csv
                        #return apoloogy("class field must not be empty", 403)
                return redirect("/")

        except FileNotFoundError:
            return apology("File not readbale", 403)

    #return apology("TODO")

@app.route("/teachers_import_students", methods=["GET", "POST"])
@login_required
def teachers_import_students():
    """Sell shares of stock"""
    if request.method == "GET":

        tchr_clss = db.execute("SELECT clsname FROM class JOIN persons ON class.cls_prsnid = persons.prsnid WHERE persons.prsnid = :ownerdb",
                            ownerdb=session['teachers'])
        #tchr_cls = tchr_clss['clsname']
        return render_template("teachers_import_students.html", tchr_class=tchr_clss)
    else:

        form_classs = request.form.get("class")

        if form_classs == "class":
            return apology("Sorry you must select students class", 403)

        csv_file = request.form.get("csv_file")

        if not re.search(".csv$", csv_file):
            return apology("sorry not a csv file", 403)

        try:
            with open(csv_file, "r") as csv_f:
                details = csv.reader(csv_f)

                if details == "":
                    return apology("sorry you must fill in correct data in the csv")

                ls_name = []
                ls_genders = []
                ls_year = []
                ls_birth = []
                ls_classs = []
                    

                for row in details:
                    name = row[0]
                    gender = row[1]
                    year = row[2]
                    birth = row[3]
                    classs = row[4]

                    #all_classes = [ class1 = for each_class in classs ]
                    ls_gender = ["f", "m", "gender"]
                    ls_class = ["js1", "js2", "js3", "ss1", "ss2", "ss3", "class"]

                    if name == "" or len(name) > 64:
                        return apology("csv file not properly filled", 403)
                    if gender not in ls_gender:
                        return apology("csv file not properly filled (gender)", 403)
                        
                    if year != "year":
                        csv_year = year
                        year_format = "%Y"
                        try:
                            datetime.strptime(csv_year, year_format)
                        except ValueError:
                            return apology("Year fromat not properly filled (YYYY)", 403)
                            

                    if birth != "birth":
                        csv_birth = birth
                        birth_format = "%d/%m/%Y" #Date format DD/MM/YYYY
                        try:
                            datetime.strptime(csv_birth, birth_format)
                        except ValueError:
                            return apology("Birth fromat not properly filled (DD/MM/YYYY)", 403)
                            


                    # Remember to put a drop down in the submission page csv_class=form_class
                    if classs != "class":
                        if classs != form_classs:
                            return apology("Class not properly filled")
                        


                    if name != "name" and gender != "gender" and year != "year" and birth != "birth" and classs != "class":
                        ls_name.append(name)
                        ls_genders.append(gender)
                        ls_year.append(year)
                        ls_birth.append(birth)
                        ls_classs.append(classs)

                for usr in range(len(ls_name)):
                    #Start identation from here 

                    usernamedb = db.execute("SELECT username FROM persons WHERE username = :usernamedb", usernamedb=ls_name[usr])

                    if len(usernamedb) != 0:
                        return apology("username already taken", 403)
                        ########################################################
                        
                for items in range(len(ls_name)):
                    # Use student name to check if their name exist
                    #print(ls_name[each])
                    #print(ls_genders[each])
                    #print(ls_year[each])
                    #print(ls_birth[each])
                    #print(ls_classs[each])
                    
                    pswd_hash = generate_password_hash("1234")

                    db.execute("INSERT INTO prsntype (prsntype) VALUES (:teacherdb)", teacherdb="student")

                    last_id = db.execute("SELECT MAX(prsntypeid) AS id FROM prsntype")

                    db.execute("INSERT INTO persons (prsntypeid, username, hash) VALUES (?, ?, ?)", last_id[0]['id'], ls_name[items], pswd_hash)

                    last_prsnid = db.execute("SELECT MAX(prsnid) AS id FROM persons")

                    db.execute("INSERT INTO studentdata (std_prsnid, stdname, std_dob, std_gender) VALUES (:tchr_prsniddb, :tchrdnamedb, :std_dobdb, :tchr_genderdb)", 
                                tchr_prsniddb=last_prsnid[0]['id'], tchrdnamedb=ls_name[items], std_dobdb=ls_birth[items], tchr_genderdb=ls_genders[items])

                    db.execute("INSERT INTO year (yrname) VALUES (:yrnamedb)", yrnamedb=ls_year[items])

                    last_yrid = db.execute("SELECT MAX(yrid) AS id FROM year")

                    #if len(classs) != 0:
                        #if len(classs) > 2:
                            #TODO FOR 3 CLASSES

                    db.execute("INSERT INTO class (cls_prsnid, cls_yrid, clsname) VALUES (:cls_prsniddb, :cls_yriddb, :clsnamedb)", 
                            cls_prsniddb=last_prsnid[0]['id'], cls_yriddb=last_yrid[0]['id'], clsnamedb=ls_classs[items])
                    
                        #else:
                            #TODO FOR 2 CLASSES
                    #else:
                        #TODO FOR 1 CLASS remember to skip the first row which is the header of the csv
                        #return apoloogy("class field must not be empty", 403)
                return redirect("/")

        except FileNotFoundError:
            return apology("File not readbale", 403)

    #return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
