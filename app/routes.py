from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db, app
from app.forms import LoginForm
from app.models import User, Post
import sqlalchemy as sa
from urllib.parse import urlsplit
from bokeh.plotting import figure
from bokeh.embed import components
from random import randint

@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Main Blog', posts=posts)

@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template('home_page.html')

@app.route('/test_graph_dashboard')
def test_graph_dashboard():
    bokeh_figure = figure(title='test scatter plot',x_axis_label='I hate my x',y_axis_label='Y am I doing this',height=400, sizing_mode='stretch_width')
    x_values=list(range(10))
    y_values=[randint(1,50) for _ in range(10)]
    bokeh_figure.circle(x_values, y_values, size=15, color='red', alpha=0.5)
    script, div = components(bokeh_figure)

    print("Generated Script:", script[:200])  # Print first 200 characters
    print("Generated Div:", div[:200])        # Print first 200 characters
    return render_template('test_graph_dashboard.html', script=script, div=div)




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

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash("Form validated successfully")
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    else:
        print("Form validation failed:", form.errors)
    return render_template('login.html', title='login page', form=form)

