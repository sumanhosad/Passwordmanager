from flask import Flask,render_template,url_for

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
