import os
import mysql.connector

from mysql.connector import connect



from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, send_file
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename



from helpers import apology, login_required, register_required, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SQLACHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root_toor@localhost/project_data'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create mysql connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root_toor",
    database="project_data"
)

db = mydb.cursor(dictionary=True)

print(db.rowcount, "record inserted.")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/")
def firstpage():
    logo_path = "static/images/LOGO_IMAGE.png"
    return render_template("firstpage.html", logo_path=logo_path)


@app.route("/hobbies", methods=["GET", "POST"])
def hobbies():
    if request.method == "POST":
        options = [request.form.get(f"option{i}") for i in range(1, 31)]
        query = "INSERT INTO hobbies (user_id, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11, question12, question13, question14, question15, question16, question17, question18, question19, question20, question21, question22, question23, question24, question25, question26, question27, question28, question29, question30) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (session["user_id"], (*options, ))
        db.executemany(query, values)
        mydb.commit()
        print(options[0], "record inserted.")
        return redirect("/interests")
    else:
        return render_template("hobbies.html")

    
    
@app.route("/interests", methods=["GET", "POST"])
#@register_required
def interests():
    #if not session.get("name"):
        #return redirect("/login")
    
    if request.method == "POST":
        
        interests = request.form.getlist("interest")
        
        for interest in interests:
            db.executemany("INSERT INTO interests (user_id, interests) VALUES (%s, %s)", (session["user_id"], interest, ))
        
        mydb.commit()

        print(db.rowcount, "record inserted.")
        
        return redirect("/profile")
    else:
        return render_template("interests.html")   


@app.route("/match")
def match():
    return render_template("match.html")



@app.route("/homepage")
def homepage():
    #if not session.get("name"):
        #return redirect("/login")
        logo_path =  "static/images/LOGO_IMAGE.png"
    
        db.execute("SELECT username FROM users WHERE id = %s", (session["user_id"],))
        username = db.fetchall()[0]["username"]
        
        db.execute("SELECT about FROM users WHERE id = %s", (session["user_id"],))
        about = db.fetchall()[0]["about"]
        
        # Use the SELECT statement to retrieve the image data from the database
        db.execute("SELECT images FROM profiles WHERE user_id= %s", (session["user_id"],))
        profile_path = db.fetchall()
        print(profile_path)
        profile_path = profile_path[0]["images"] if profile_path else "default.jpg"
        
        
        db.execute("SELECT username FROM users WHERE user_id IN (SELECT user_id FROM interests WHERE interest IN (SELECT interest FROM interests WHERE user_id = %s", session["user_id"])
        usernames = db.fetchall()
        return render_template("/homepage.html", username=username, about=about, profile_path=profile_path, logo_path=logo_path, usernames=usernames)
        
        

@app.route("/profile", methods=["GET", "POST"])
def profile():
    #if not session.get("name"):
        #return redirect("/login")
            
    if request.method == "POST":
        
        profile_picture = request.files['image']
        profile_path = f"static/uploads/{profile_picture}"
        
        if profile_picture:
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture.filename))
            print('Image uploaded successfully!')
            
            # Use the INSERT statement to save the file to the database
            sql = "INSERT INTO profiles (user_id, images) VALUES (%s, %s)"
            val = (session["user_id"], profile_picture.filename, )
            db.execute(sql, val)
            mydb.commit()
            print ('File uploaded successfully')
            return redirect("/homepage")
        else:
            print('/error')
    
    else:
        db.execute("SELECT username FROM users WHERE id = %s", (session["user_id"],))
        username = db.fetchall()[0]["username"]
        
        db.execute("SELECT about FROM users WHERE id = %s", (session["user_id"],))
        about = db.fetchall()[0]["about"]
        
        db.execute("SELECT images FROM profiles WHERE user_id= %s", (session["user_id"],))
        profile_path = db.fetchall()
        print(profile_path)
        profile_path = profile_path[0]["images"] if profile_path else "default.jpg"
        
        return render_template("profile.html", username=username, about=about, profile_path=profile_path)



@app.route("/myprofile", methods=["GET", "POST"])
def myprofile():
    #if not session.get("name"):
        #return redirect("/login")
    if request.method == "POST":
        profile_picture = request.files['image']
        new_profile_path = f"static/uploads/{profile_picture}"
        
        if profile_picture:
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_picture.filename))
            print('Image uploaded successfully!')
            print(new_profile_path, session["user_id"])
            # Use the UPDATE statement to update the file in the database
            db.execute("UPDATE profiles SET images = %s WHERE user_id = %s", (profile_picture.filename, session["user_id"],))
            mydb.commit()
            
            print ('File updated successfully')
            return redirect("/homepage")
    else:
        db.execute("SELECT username FROM users WHERE id = %s", (session["user_id"],))
        username = db.fetchall()[0]["username"]
        
        db.execute("SELECT about FROM users WHERE id = %s", (session["user_id"],))
        about = db.fetchall()[0]["about"]
        
        # Use the SELECT statement to retrieve the image data from the database
        db.execute("SELECT images FROM profiles WHERE user_id= %s", (session["user_id"],))
        profile_path = db.fetchall()
        print(profile_path)
        profile_path = profile_path[0]["images"] if profile_path else "default.jpg"
        
        return render_template("myprofile.html", username=username, about=about, profile_path=profile_path)
        


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide valid email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        email = request.form.get("email")
        db.execute("SELECT * FROM users WHERE email = %s", (email,))
        rows = db.fetchall()
        #sql = "SELECT * FROM users WHERE email = %s"
        #val = (request.form.get("email"))
        #print(val)
        ##rows = db.execute(sql, (val,))
        
        print(rows)

        # Ensure email exists and password is correct
        if len(rows) != 1:
            return apology("invalid email 403")
        
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid password 403")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/homepage")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        logo_path = "static/images/LOGO_IMAGE.png"
        return render_template("login_register.html", logo_path=logo_path)


@app.route("/logout")
def logout():
    """Log user out"""
    session["name"] = None

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
        

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    
    if request.method == "POST":
    
        fullname = request.form.get("fullname")
        email = request.form.get("email")
        password = request.form.get("password")
        about = request.form.get("about")
        
        if not fullname:
            return apology("fullname required")
        elif not password:
            return apology("password required")
        #elif len(password) != 8:
            #return apology("Length of password must be 8 characters")
        elif not about:
            return apology("About you is required")
        
        #if password != confirmation:
            #return apology("passwords do not match")
        
        
        hash = generate_password_hash(password)
        
        sql = "INSERT INTO users (username, hash, email, about) VALUES (%s, %s, %s, %s)"
        val = (fullname, hash, email, about)
        db.execute(sql, val)
        
        
        mydb.commit()
        

        print(db.lastrowid, "record inserted.")
        
        session["user_id"] = db.lastrowid

        #sql = "INSERT INTO profiles (user_id) VALUES (%s) WHERE user_id = %s AND profile_id = %s" 
        #val = (user_id)
       # db.execute(sql, val)
        
       # mydb.commit()
       
       # print(db.rowcount, "record inserted.")
        return redirect("/hobbies")
    
    else:
        return render_template("login_register.html")



#val = (session["user_id"], (option1,), (option2,), (option3,), (option4,), (option5,), (option6,), (option7,), (option8,), (option9,), (option10,), (option11,), (option12,), (option13,), (option14,), (option15,), (option16,), (option17,), (option18,), (option19,), (option20,), (option21,), (option22,), (option23,), (option24,), (option25,), (option26,), (option27,), (option28,), (option29,), (option30,))