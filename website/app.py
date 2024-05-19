import random
import json
import base64
import string
from sqlalchemy import String, Column
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime, timedelta
from website.encryption import generate_key, encrypt_message, decrypt_message

db = SQLAlchemy()


class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    master_password = db.Column(db.String(100), nullable=False)
    passwords = db.Column(db.Text, nullable=True)  # Store passwords as a JSON string

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
                return redirect(url_for("home"))
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

    
    @app.route('/addpassword', methods=['GET', 'POST'])
    def addpassword():
        if(session["user"]==None):
            return redirect(url_for("login"))
        user=session.get('user')
        if request.method == 'POST':
        # Extract form inputs
            website_details = [
                request.form['website'],
                request.form['url'],
                request.form['email'],
                request.form['username'],
                request.form['password']
            ]

        # Encrypt password details
            mp = session.get('mp')
            if mp is None:
                # Handle case where master password is not in session
                return "Error: Master password not found in session."

            encrypted_message = encrypt_message(website_details, mp)

            # Update user record with encrypted details
            userdata = User.query.filter_by(username=session.get("user")).first()
            user=userdata.username
            if userdata is None:
                # Handle case where user record does not exist
                return "Error: User not found."
            existpassword=retrieve_passwords(user)
            if existpassword==None:
                replace_passwords(user,encrypted_message)
                db.session.commit()
            else:
                passwords='||'.join([existpassword , encrypted_message])
                replace_passwords(user,passwords)
                db.session.commit()
            # Redirect to the same page to clear form data
            return redirect(url_for("addpassword"))
        else:
            # Render the addpassword.html template for GET requests
            return render_template('addpassword.html')
        

    @app.route('/accesspassword')
    def accesspassword():
        if "user" not in session:
            return redirect(url_for('login'))

        username = session["user"]
        encrypted_details = retrieve_passwords(username)
    
        if encrypted_details is None:
                return redirect(url_for('login'))

        decrypted_details = {}
        try:
            for column, encrypted_message in encrypted_details.items():
                decrypted_message = decrypt_message(encrypted_message, session["mp"])
                decrypted_details[column] = decrypted_message
        except Exception as e:
            app.logger.error("Error decrypting password details for user: %s (%s)", username, str(e))
            return "Error decrypting password details. Please try again later."

        return render_template('accesspassword.html', message=decrypted_details)
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

def retrieve_passwords(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.passwords
    else:
        return None


def replace_passwords(username, new_passwords):
    user = User.query.filter_by(username=username).first()

    if user:
        user.passwords = new_passwords
        db.session.commit()
        return True
    else:
        return False
