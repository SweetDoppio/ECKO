from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.forms import LoginForm
from app.models import User, Post
import sqlalchemy as sa
from urllib.parse import urlsplit

def configure_routes(app):
    @app.route('/index')
    @login_required
    def index():
        posts = Post.query.all()
        return render_template('index.html', title='Main Blog', posts=posts)

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

