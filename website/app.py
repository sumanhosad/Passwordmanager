from flask import Flask,render_template,url_for,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from rich.console import Console
console = Console()


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'passwordmanager'
    
    @app.route('/login', methods=["POST","GET"])
    def login():
        session.pop("user",None)
        if request.method=="POST":
            user=request.form["username"]
            session["user"]=user
            return redirect(url_for("home",usr=user))
        else:
            session.clear()
            return render_template('login.html')
    @app.route('/')
    def home():
        if "user" in session:
            user=session["user"]
            return render_template('homepage.html')
        else:
            return render_template('login.html')
    @app.route('/signin',methods=["POST","GET"])
    def signin():
        if request.method=="POST":
            user=request.form["username"]
            session["user"]=user
            return redirect(url_for("home",usr=user))
        else:
            return render_template('signin.html',methods = ['GET', 'POST'])

    @app.route('/addpassword')
    def addpassword():
        return render_template('addpassword.html')

    @app.route('/accesspassword')
    def accesspassword():
        return render_template('accesspassword.html')
    
    @app.route('/managepassword')
    def managepassword():
        return render_template('managepassword.html')
  
    return app

def create_databse(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    db = SQLAlchemy(app)


