import re
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
    if not session.get("user_id"):
        return redirect("/login")
    
    if request.method == "POST":
        options = [request.form.get(f"option{i}") for i in range(1, 31)]
        query = "INSERT INTO hobbies (user_id, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10, question11, question12, question13, question14, question15, question16, question17, question18, question19, question20, question21, question22, question23, question24, question25, question26, question27, question28, question29, question30) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (session["user_id"], *options)
        db.execute(query, values)
        mydb.commit()
        print(options[0], "record inserted.")
        return redirect("/interests")
    else:
        return render_template("hobbies.html")

    
    
@app.route("/interests", methods=["GET", "POST"])
#@register_required
def interests():
    if not session.get("user_id"):
        return redirect("/login")
    
    if request.method == "POST":
        
        interests = request.form.getlist("interest")
        
        for interest in interests:
            db.execute("INSERT INTO interests (user_id, interest) VALUES (%s, %s)", (session["user_id"], interest, ))
        
        mydb.commit()

        print(db.rowcount, "record inserted.")
        
        return redirect("/profile")
    else:
        return render_template("interests.html")   


@app.route("/match")
def match():
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("match.html")



@app.route("/homepage")
def homepage():
    if not session.get("user_id"):
        return redirect("/login")
    
    logo_path =  "static/images/LOGO_IMAGE.png"

    db.execute("SELECT username FROM users WHERE id = %s", (session["user_id"],))
    username = db.fetchall()[0]["username"]
    
    db.execute("SELECT about FROM users WHERE id = %s", (session["user_id"],))
    about = db.fetchall()[0]["about"]
    
    # Use the SELECT statement to retrieve the image data from the database
    db.execute("SELECT images FROM profiles WHERE user_id= %s", (session["user_id"],))
    profile_path = db.fetchall()
    #print(profile_path)
    profile_path = profile_path[0]["images"] if profile_path else "default.jpg"
    
    
    
    #Fetch the users hobbies
    db.execute("SELECT * FROM hobbies  WHERE user_id = %s", (session["user_id"], ))
    user_hobby = db.fetchall()[0]

    # execute the SELECT statement and fetch the results
    db.execute("SELECT users.username, hobbies.* FROM hobbies JOIN users ON users.id = hobbies.user_id WHERE user_id != %s", (session["user_id"], ))
    hobbies = db.fetchall()
    print(hobbies)
    
    names_list = []

    # iterate over each row in the hobbies list
    for hobby in hobbies:
        num_match = 0

        # check for a match between the current row and the user_hobby dictionary
        for i in range(1, 31):
            if f"question{i}" in hobby and user_hobby:
                num_match += 1 if hobby[f"question{i}"] == user_hobby[f"question{i}"] else 0
                print(hobby[f"question{i}"],"...")
                print(user_hobby[f"question{i}"])

        user_num_match = 30
        # calculate the match percentage
        match_percentage = (user_num_match / 100) * 70
        match_percentage = round(match_percentage)
        # if the match percentage is at least 70%, append the names value to the names_list
        if num_match >= match_percentage:
            names_list.append(hobby["username"])
            print(names_list)
            print(num_match)
            
            
    # Convert the names_list to a string that can be used as an argument to the IN operator
    names_string = ', '.join(['%s'] * len(names_list))

    # Use the SELECT statement to retrieve the image data from the database
    db.execute("SELECT images FROM profiles JOIN users ON users.id = profiles.user_id WHERE username IN ({names_string})".format(names_string=names_string), names_list)
    user_profile_paths = db.fetchall()

    # Zip the names_list and user_profile_paths together so that we can access both in the Jinja template
    names_and_profiles = zip(names_list, user_profile_paths)
                
    return render_template("/homepage.html", username=username, about=about, profile_path=profile_path, logo_path=logo_path, names_list=names_list, names_and_profiles=names_and_profiles)
        
        

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user_id"):
        return redirect("/login")
            
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
            return redirect("/match")
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
    if not session.get("user_id"):
        return redirect("/login")
    
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

        # Query database for email
        email = request.form.get("email")
        db.execute("SELECT * FROM users WHERE email = %s", (email,))
        rows = db.fetchone()
        # If email is not in database, return apology
        if not rows:
            return apology("Email does not exist!")
        
        # Check if password is correct
        if not check_password_hash(rows["hash"], request.form.get("password")):
            return apology("Invalid password")
        
        # Remember which user has logged in
        session["user_id"] = rows["id"]
        
        # Redirect user to homepage
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
    return redirect("/login")
        

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure fullname, email, and password were submitted
        if not request.form.get("fullname"):
            return apology("fullname required")
        elif not request.form.get("email"):
            return apology("email required")
        elif not request.form.get("password"):
            return apology("password required")
        elif not request.form.get("about"):
            return apology("about required")
        
        # Validate email format
        email = request.form.get("email")
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return apology("Invalid email")

        # Hash the password
        password = request.form.get("password")
        hash = generate_password_hash(password)

        # Check if the email entered by the user is already in the database
        db.execute('SELECT email FROM users WHERE email = %s', (email,))
        if db.fetchone():
            return apology("Email already exists in the database")

        # Insert the fullname, email, hashed password, and about information into the database
        db.execute('INSERT INTO users (username, hash, email, about) VALUES (%s, %s, %s, %s)', (request.form.get("fullname"), hash, email, request.form.get("about")))
        mydb.commit()

        # Remember which user has logged in
        session["user_id"] = db.lastrowid

        print(db.lastrowid, "record inserted.")
        return redirect("/hobbies")
    
    else:
        return render_template("login_register.html")

#val = (session["user_id"], (option1,), (option2,), (option3,), (option4,), (option5,), (option6,), (option7,), (option8,), (option9,), (option10,), (option11,), (option12,), (option13,), (option14,), (option15,), (option16,), (option17,), (option18,), (option19,), (option20,), (option21,), (option22,), (option23,), (option24,), (option25,), (option26,), (option27,), (option28,), (option29,), (option30,))