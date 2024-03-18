from flask import Flask,render_template,url_for
import mysql.connector
from rich.console import Console
console = Console()


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'passwordmanager'   
       

    @app.route('/login')
    def login():
        return render_template('login.html')
    @app.route('/')
    def home():
        return render_template('homepage.html')
    return app


  
def dbconfig():
  try:
    db = mysql.connector.connect(
      host ="localhost",
      user ="root",
      passwd ="password"
    )
    print("Connected to db")
  except Exception as e:
    print("An error occurred while trying to connect to the database")
    console.print_exception(show_locals=True)

  return db
