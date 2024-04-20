import random
import string
from sqlalchemy import String
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime, timedelta
from website.database import generate_key, encrypt_message, decrypt_message
db = SQLAlchemy()

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    master_password = db.Column(db.String(100), nullable=False)

    @classmethod
    def add_column(cls, column_name, column_type=String(50), nullable=False):
        """
        Add a new column to the User table dynamically.
        """
        # Check if the column already exists
        if column_name in cls.__table__.columns:
            print(f"Column '{column_name}' already exists.")
            return

        # Add the new column to the User table
        new_column = Column(column_name, column_type, nullable=nullable)
        new_column_name = cls.__tablename__ + '_' + column_name  # Generate unique column name
        new_column.name = new_column_name
        cls.__table__.append_column(new_column)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'passwordmanager'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwordmanager.db'

    db.init_app(app)
    with app.app_context():
        db.create_all()


    @app.route('/login', methods=["POST","GET"])
    def login():
        session.pop("user", None)
        if request.method == "POST":
            user = request.form["username"]
            master_password = request.form["password"]
            existing_user = User.query.filter_by(username=user).first()
            if existing_user==None:
                return render_template('login.html', message="Username doesn't exists.")   
            if existing_user and existing_user.master_password == hash_password(master_password):
                session["user"] = user
                session["mp"]=hash_password(master_password)
                return redirect(url_for("home", usr=user))
            else:
                return redirect(url_for("login"))

        else:
            session.clear()
            return render_template('login.html')
    @app.route('/')
    def home():
        if "user" in session:
            user = session["user"]
            return render_template('homepage.html')
        else:
            return render_template('login.html')

    @app.route('/signin', methods=["POST","GET"])
    def signin():
        if request.method == "POST":
            user = request.form["username"]
            mp=request.form["password"]
            hashed_mp = hash_password(mp)
            
            existing_user = User.query.filter_by(username=user).first()
            if existing_user:
                return render_template('signin.html', message="Username already exists. Please choose a different username.")            
            
            session["user"] = user
            useradd(user, hashed_mp)
            db.create_all()
            return redirect(url_for("home", usr=user))
        else:
            return render_template('signin.html')

    @app.route('/<usr>')
    def usr(usr):
        return redirect(url_for('home', usr=usr))

    @app.route('/addpassword')
    def addpassword():
        if request.method == 'POST':
            # Get form inputs and store them in a listwebsite_details
            website_details = [
                request.form['website'],
                request.form['url'],
                request.form['email'],
                request.form['username'],
                request.form['password']
            ]
            # Encrypt the website detailsencrypted_message
            encrypted_message = encrypt_message(website_details, mp)
            User.add_column(website_details[0])
        else:
            return render_template('addpassword.html')

        
 
    @app.route('/accesspassword')
    def accesspassword():
        return render_template('accesspassword.html')

    @app.route('/managepassword')
    def managepassword():
        return render_template('managepassword.html')

    return app

def useradd(username, master_password):
    new_user = User(username=username, master_password=master_password)
    db.session.add(new_user)
    db.session.commit()

def adduserpasswordtable(website, url, email, usernames, password):
    print()

def hash_password(mp):
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    return hashed_mp

def generatePassword(length):
	return ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation ) for n in range(length)])
