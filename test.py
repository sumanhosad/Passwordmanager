from flask import Flask,redirect,url_for

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Welcome to My Flask Webpage!</h1>'


@app.route('/<name>')
def usr(name):
    return (f"Hello {name}")

@app.route("/admin")
def admin():
    return redirect(url_for("home"))
if __name__ == '__main__':
    app.run(debug=True)
