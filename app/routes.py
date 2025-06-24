from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db, app
from app.forms import LoginForm, RegisterForm
from app.models import User, Post
import sqlalchemy as sa
from urllib.parse import urlsplit
from bokeh.plotting import figure
from bokeh.embed import components
from random import randint
import json
import os

# Define the static folder path explicitly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
app.static_folder = STATIC_FOLDER

# Path to quiz.json
QUIZ_JSON_PATH = os.path.join(app.static_folder, 'quiz.json')

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

@app.route('/quiz')
def quiz():
        return render_template('quiz.html')

@app.route('/edit_quiz', methods=['GET', 'POST'])
def edit_quiz():
    if request.method == 'POST':
        try:
            # Get form data
            questions = []
            for i in range(len(request.form) // 8):  # Assuming 3 options per question
                question = {
                    'index': i,
                    'question': request.form.get(f'question_{i}'),
                    'options': [
                        {'value': 'a', 'text': request.form.get(f'option_{i}_a')},
                        {'value': 'b', 'text': request.form.get(f'option_{i}_b')},
                        {'value': 'c', 'text': request.form.get(f'option_{i}_c')}
                    ],
                    'correct': request.form.get(f'correct_{i}')
                }
                questions.append(question)
            
            # Save to quiz.json
            with open(QUIZ_JSON_PATH, 'w') as f:
                json.dump({'questions': questions}, f, indent=2)
            return redirect(url_for('quiz'))
        except Exception as e:
            return render_template('edit_quiz.html', error=str(e))
    
    # Load existing quiz data for editing
    try:
        with open(QUIZ_JSON_PATH) as f:
            quiz_data = json.load(f)
        return render_template('edit_quiz.html', questions=quiz_data['questions'])
    except FileNotFoundError:
        return render_template('edit_quiz.html', questions=[], error="quiz.json not found")

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/register')
def register():
    reg_form = RegisterForm()
    return render_template('register.html')

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

