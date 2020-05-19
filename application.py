# import os
from flask import Flask, session, render_template, url_for, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session.__init__ import Session
from flask_sqlalchemy import sqlalchemy
# from application import app

app = Flask(__name__)

# set database connection string
if os.getenv("DATABASE_URL") == None:
    dbconnection = "postgres://neirzwjdfklgwv:06ddc2eb1be9201f1324c6779bb86b764d2fb843df91d38af3c9d1da4df25459@ec2-54-81-37-115.compute-1.amazonaws.com:5432/d4gljnrpedu0op"
else:
    dbconnection = os.getenv("DATABASE_URL")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "thisisthesecretkey"
Session(app)

engine = create_engine(dbconnection)
db = scoped_session(sessionmaker(bind=engine))
db = sqlalchemy(app)

@app.route("/",methods=["GET","POST"])
def register():
    variable = ""
    if request.method == "POST":

        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            email = request.form.get('email')
            if email == " ":
                raise ValueError
        except ValueError:
            print("Please enter valid credentials")    

        # if len(email.strip()) or len(username.strip()) or len(password.strip()) == 0:
        # if email or username or password == " ":
            # return "Invalid Credentials. Please try again."
        # else:

        result = db.execute("SELECT username from userinfo where username = :user ",{"user":username}).fetchone()
        if result is None:
            db.execute("INSERT INTO userinfo(username,password,email) VALUES(:user,:pass,:email)", {"user":username, "pass":password, "email":email})
            db.commit()
        return redirect(url_for('login'))

        # else:
        #    flash("USer already exists")
        #    return render_template(url_for('login'))    

    else:
        return render_template("register.html",variable=variable)    

# @app.before_request
# def before_request():
    # g.var = user        


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":

        user = request.form.get("user")
        passwords = request.form.get("user_password")
    
        session['username'] = user #set the value

        if db.execute("SELECT username,password from userinfo where username = :userName and password = :Password",
        {"userName":user,"Password":passwords}).rowcount == 0:
            return "Invalid Username/Password, Please try again"
        else:
            return redirect(url_for('getdashboard'))
    else:
        return render_template("login.html")

@app.route("/dashboard",methods=["GET"])
def getdashboard():
    if "username" in session:
        return render_template("dashboard.html")
    else:
        return redirect(url_for('login'))    

@app.route("/dashboard",methods=["POST"])
def postdashboard():
    bookinfo = request.form.get("searchbar")
    storedData = [] #creating a list to store the data, if it matches the database.
    # search into books table by keyword   
    if db.execute("SELECT isbn, author, title, year from books WHERE isbn = :isbn or author = :isbn or title = :isbn", {"isbn":bookinfo}).rowcount == 0:
        return render_template("error.html",message="No such book Found")
    else:
        queriedata = db.execute("SELECT isbn, author, title, year from books WHERE isbn = :isbn or author = :isbn or title = :isbn", {"isbn":bookinfo}).fetchall()
        storedData.append(queriedata)
        return render_template("reviews.html")
        # return redirect(url_for('reviews'))

@app.route("/reviews")
def reviews():
    pass        

        
@app.errorhandler(405)
def error(message):
    return render_template("error.html",message="You have some error in your code")

# @app.route("/reviews",methods=["GET","POST"])
# def reviews():
    # if redirect.method == "POST":
        # db.execute("")


@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)