from flask import Flask, render_template, request, session, redirect, url_for
import db_builder
from game import Game

app = Flask(__name__)
app.secret_key = 'minesweeper'

def logged_in():
    return session.get('username') is not None

@app.route('/', methods=['GET','POST'])
def login():
    method = request.method
    # Check for session existance
    if method == 'GET':
        if logged_in():
            return redirect('/menu')
        else:
        # If not logged in, show login page
            return render_template('login.html', error=False)

    if method == 'POST':
    # Get information from request.form since it is submitted via post
        username = request.form['username']
        password = request.form['password']
        error = db_builder.login(username, password)

    if error:
    # If incorrect, give feedback to the user
        return render_template('login.html', error=error)
    else:
    # Store user info into a cookie
        session['username'] = username
        return redirect('/menu')

@app.route('/register', methods=['GET','POST'])
def register():
    method = request.method
    # Check for session existence
    if method == "GET":
        if logged_in():
            return redirect('/')
        else:
            # If not logged in, show regsiter page
            return render_template('register.html', error_message="")

    if method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        confirm_password = request.form["confirm_password"]

        error_message = ""
        if not new_username:
            error_message = "Error: No username entered!"
        elif not new_password:
            error_message = "Error: No password entered!"
        elif confirm_password != new_password:
            error_message = "Error: Passwords do not match!"

        if error_message:
            return render_template("register.html", error_message=error_message)

        error_message = db_builder.signup(new_username, new_password)

        if error_message:
            return render_template("register.html", error_message=error_message)
        else:
            session['username'] = new_username
            return redirect('/')

@app.route('/loading')
def load():
    try:
        return render_template("load.html")
    except:
        return render_template("error.html")

@app.route('/menu')
def menu():
    try:
        return render_template("menu.html")
    except:
        return render_template("error.html")

@app.route('/gamepage')
def about():
    try:
        return render_template("gamepage.html")
    except:
        return render_template("error.html")
        
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True
    app.run()