from flask_app import app
from flask import render_template, redirect,request,session,flash
import re
from flask_app.models.user import User
from flask_app.models.post import Post
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Render the index page with login and register
@app.route('/')
def login_reg():
    return render_template('index.html')

#the route used to manipulate the data and call to insert it into the database
@app.route('/register', methods=['POST'])
def create_user():
    usernamedata = {'username': request.form['username']}
    data = {'email': request.form['email']}
    username_in_db = User.get_by_username(usernamedata)
    user_in_db = User.get_by_email(data)
    if not User.validate_user(request.form):
        return redirect('/')

    if username_in_db:
        flash('An account with that username already exists.')
        return redirect('/')

    if user_in_db:
        flash('Email already exists. Please Log In')
        return redirect('/')
    passhash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'fname' : request.form['fname'],
        'lname' : request.form['lname'],
        'email' : request.form['email'],
        'username' : request.form['username'],
        'password' : passhash
    }
    user_id = User.save_user(data)
    session['user_id'] = user_id
    session['username'] = data['username']
    return redirect('/dashboard')

#the route used to log in
@app.route('/login', methods=['POST'])
def login():

    data = {'email': request.form['email']}

    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash('Invalid Email')
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid Password')
        return redirect('/')
    
    session['user_id'] = user_in_db.id
    session['username'] = user_in_db.username

    return redirect('/dashboard')

#The route used to render the dashboard page
@app.route('/dashboard')
def logged_in():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    
    return render_template('dashboard.html',
                            username = session['username'],
                            user_id = session['user_id'],
                            posts = Post.getallposts()
                           )

#a route for logging out
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#a route for rendering the my account tab
@app.route('/mypage')
def myaccount():
    if 'user_id' not in session:
        flash('Must login')
        return redirect('/')
    
    return render_template('myaccount.html', posts = Post.getpostsbyuserid({'id' :session['user_id']}))

#a route used for rendering a users page
@app.route("/page/<id>")
def userPage(id):
    if 'user_id' not in session:
        flash('Must Login')
        return redirect('/')
    return render_template("page.html", posts = Post.getpostsbyuserid({"id" : id}), user = User.get_by_id({"id" : id}))