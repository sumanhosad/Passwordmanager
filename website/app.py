
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    master_password = db.Column(db.String(100), nullable=False)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sitename = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    user = db.relationship('User', backref=db.backref('passwords', lazy=True))

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'passwordmanager'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwordmanager.db'

    init_db(app)

    @app.route('/login', methods=["POST","GET"])
    def login():
        session.pop("user", None)
        if request.method == "POST":
            user = request.form["username"]
            master_password=request.form["password"]
            session["user"] = user
            return redirect(url_for("home", usr=user))
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
                return redirect(url_for('login'))
            
            session["user"] = user
            useradd(user, hashed_mp)
            return redirect(url_for("home", usr=user))
        else:
            return render_template('signin.html')

    @app.route('/<usr>')
    def usr(usr):
        return redirect(url_for('home', usr=usr))

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

def useradd(username, master_password):
    new_user = User(username=username, master_password=master_password)
    db.session.add(new_user)
    db.session.commit()

def hash_password(mp):
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    return hashed_mp

