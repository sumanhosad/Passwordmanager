import random
import string
from sqlalchemy import String
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime, timedelta
from website.encryption import generate_key, encrypt_message, decrypt_message
db = SQLAlchemy()

# Define global variables
mp = None
user = None

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    master_password = db.Column(db.String(100), nullable=False)
    @classmethod 
    def add_column(cls, column_name, column_type=String(50), nullable=False):
        # Check if the column already exist 
        if column_name in cls.__table__.columns:
            return f"Column '{column_name}' already exists."

         # Define the new column
        new_column = db.Column(column_name, column_type, nullable=nullable)

        # Add the column to the User table metadata
        cls.__table__.append_column(new_column)

        # Reflect the change in the class attributes
        setattr(cls, column_name, new_column)

    @classmethod 
    def view_columns(cls):
        excluded_columns = ['username', 'master_password']
        columns = []

        # Iterate through the columns and exclude the ones in the exclusion list
        for column_name, column in cls.__table__.columns.items():
            if column_name not in excluded_columns:
                columns.append(column_name)

        return columns


    @staticmethod
    def get_encrypted_details(username):
        user = User.query.filter_by(username=username).first()
        if user:
            encrypted_details = {}
            columns = user.view_columns()
            for column in columns:
                # Exclude username and master_password columns
                if column not in ['username', 'master_password']:
                    encrypted_message = getattr(user, column)
                    if encrypted_message:
                        encrypted_details[column] = encrypted_message
            return encrypted_details
        else:
            return None

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
            if existing_user is None:
                return render_template('login.html', message="Username doesn't exists!!")   
            if existing_user and existing_user.master_password == hash_password(master_password):
                session["user"] = user
                session["mp"]=hash_password(master_password)
                mp=session['mp']
                return redirect(url_for("home", usr=user))
            else:
                return render_template('login.html', message="Password Doesnt MAtch!!")   

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
            session["mp"] = hashed_mp
            mp= session['mp']
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
            mp=session['mp']
            encrypted_message = encrypt_message(website_details, mp)
            User.add_column(website_details[0])
            user = User.query.filter_by(username=session["user"]).first()
            setattr(user, website_details[0], encrypted_message)  # Assuming 'website' is the name of the new columns   
            db.session.commit()
            return redirect(url_for("addpassword"))
        else:
            return render_template('addpassword.html')
        

    @app.route('/accesspassword')
    def accesspassword():
        if "user" not in session:
            return redirect(url_for('login'))

        username = session["user"]
        encrypted_details = User.get_encrypted_details(username)

        if encrypted_details is None:
            return redirect(url_for('login'))  # Or handle appropriately

        decrypted_details = {}
        for column, encrypted_message in encrypted_details.items():
            decrypted_message = decrypt_message(encrypted_message, session["mp"])
            decrypted_details[column] = decrypted_message
    
        return render_template('accesspassword.html', decrypted_details=decrypted_details)


    @app.route('/managepassword')
    def managepassword():
        return render_template('managepassword.html')

    return app

def useradd(username, master_password):
    new_user = User(username=username, master_password=master_password)
    db.session.add(new_user)
    db.session.commit()

def hash_password(mp):
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    return hashed_mp

