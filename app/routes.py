from app import app
from flask import render_template, flash, redirect,url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import Post, User
import sqlalchemy as sa
from urllib.parse import urlsplit
from app import db
#Imported LoginForm class from forms.py and instantiate an object

@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Main Blog', posts=posts)
    #Above function takes template filename and variable list of template arguments.


#set to default page for now 
@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template('home_page.html')


@app.route('/help_page')
def help_page():
    return render_template('help_page.html')


@app.route('/tut_link')
def tut_link():
    return render_template('tut_link.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
#GET requests return info to the client, POST sends data from the browser to the server
def login():
    if current_user.is_authenticated:
        #ensures is user session is currently active, site does not redirect to login page
        return redirect(url_for('index'))
    form = LoginForm()
    #Imports the LoginForm class from app.py and instanitates an object from it.
    if form.validate_on_submit():
        flash("Form validated successfully") #check flask shell
        user = db.session.scalar(sa.select(User).where(User.username==form.username.data))
        #query user from the database
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #this  function register user as logged in, meaning any pages navigated will have current_user
        #set to that user
        next_page=request.args.get('next')
        #Flask provides a request variable that contains all
        # the information that the client sent with the request
        #request.args variable exposes contents of query stirng in dict format.
        if not next_page or urlsplit(next_page).netloc !='':
        #to avoid malicious url injections, use urlsplit then check if netloc component is set to see
        #if URL path is absolute or relative.
            next_page=url_for('index')
        #basically redirects user back to the page they wanted after they've logged in.
        #Otherwise just take to index page
        return redirect(next_page)
    else:
        print("Form validation failed:", form.errors)  
    #If browser sends POST method, and at least one of the validators retux rn 'False', function returns 'False'
    return render_template('login.html', title='login page' ,form=form) 
    #Uses the form object and passess it into a variable
    #Browser sends GET request to recieve the login form, and this will return 'False',and will skip to render_template

