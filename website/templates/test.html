
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'passwordmanager'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwordmanager.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    master_password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def create_passwords_table(username):
    class_name = f'{username.capitalize()}Password'
    return type(class_name, (db.Model,), {
        '__tablename__': f'{username}_passwords',
        'id': db.Column(db.Integer, primary_key=True),
        'urlname': db.Column(db.String(100), nullable=False),
        'url': db.Column(db.String(200), nullable=False),
        'username': db.Column(db.String(50), nullable=False),
        'password': db.Column(db.String(100), nullable=False),
        'user_id': db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False),
        'user': db.relationship(User)
    })

@app.route('/login', methods=["POST","GET"])
def login():
    session.pop("user", None)
    if request.method == "POST":
        user = request.form["username"]
        master_password = request.form["password"]
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
        mp = request.form["password"]
        hashed_mp = hash_password(mp)
        
        existing_user = User.query.filter_by(username=user).first()
        if existing_user:
            return render_template('signin.html', error='User already exists')
        
        session["user"] = user
        useradd(user, hashed_mp)
        create_passwords_table(user)  # Create a new password table for the user
        return redirect(url_for("home", usr=user))
    else:
        return render_template('signin.html')

@app.route('/<usr>')
def usr(usr):
    return redirect(url_for('home', usr=usr))

@app.route('/addpassword', methods=["POST", "GET"])
def addpassword():
    if request.method == "POST":
        sitename = request.form["sitename"]
        url = request.form["url"]
        username = request.form["username"]
        password = request.form["password"]
        
        current_user = User.query.filter_by(username=session.get("user")).first()
        if current_user:
            password_table = create_passwords_table(current_user.username)
            new_password = password_table(urlname=sitename, url=url, username=username, password=password, user_id=current_user.id)
            db.session.add(new_password)
            db.session.commit()
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template('addpassword.html')

def useradd(username, master_password):
    new_user = User(username=username, master_password=master_password)
    db.session.add(new_user)
    db.session.commit()

def hash_password(mp):
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    return hashed_mp

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
