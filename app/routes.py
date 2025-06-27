from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import db, app
from app.forms import LoginForm, RegisterForm
from app.models import User, Post
from app.scanner import Scanner
import sqlalchemy as sa
from urllib.parse import urlsplit
import email_validator

import json
import os

# Define the static folder path explicitly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
app.static_folder = STATIC_FOLDER

# Path to quiz.json
QUIZ_JSON_PATH = os.path.join(app.static_folder, 'quiz.json')

from sqlalchemy.exc import IntegrityError


@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Main Blog', posts=posts)

@app.route('/')
@app.route('/home_page')
def home_page():
    return render_template('home_page.html', title='EHKO home')



@app.route('/quiz.')
def quiz():
        return render_template('quiz.html')
    
    
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


@app.route('/edit_quiz', methods=['GET', 'POST'])
def edit_quiz():
    try:
        with open(QUIZ_JSON_PATH) as f:
            quiz_data = json.load(f)
    except FileNotFoundError:
        quiz_data = {'questions': []}

    if request.method == 'POST':
        try:
            action = request.form.get('action')
            if action == 'edit':
                index = int(request.form.get('question_index'))
                if 0 <= index < len(quiz_data['questions']):
                    quiz_data['questions'][index] = {
                        'index': index,
                        'question': request.form.get('question'),
                        'options': [
                            {'value': 'a', 'text': request.form.get('option_a')},
                            {'value': 'b', 'text': request.form.get('option_b')},
                            {'value': 'c', 'text': request.form.get('option_c')}
                        ],
                        'correct': request.form.get('correct')
                    }
            elif action == 'add':
                new_index = len(quiz_data['questions'])
                new_question = {
                    'index': new_index,
                    'question': request.form.get('question'),
                    'options': [
                        {'value': 'a', 'text': request.form.get('option_a')},
                        {'value': 'b', 'text': request.form.get('option_b')},
                        {'value': 'c', 'text': request.form.get('option_c')}
                    ],
                    'correct': request.form.get('correct')
                }
                quiz_data['questions'].append(new_question)

            with open(QUIZ_JSON_PATH, 'w') as f:
                json.dump(quiz_data, f, indent=2)
            return redirect(url_for('edit_quiz'))
        except Exception as e:
            return render_template('edit_quiz.html', questions=quiz_data['questions'], error=f"Error saving quiz: {str(e)}")

    return render_template('edit_quiz.html', questions=quiz_data['questions'])

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')

@app.route('/contact')
def contact():
    return render_template('contact.html', title='Contact Us')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/register',  methods=['GET', 'POST'])
def register():
    reg_form = RegisterForm()

    if current_user.is_authenticated:
        redirect(url_for('index'))

    if reg_form.validate_on_submit():
        try:
            new_reg_user = User(username = reg_form.username.data, email = reg_form.email.data)
            new_reg_user.set_password(reg_form.password.data)
            db.session.add(new_reg_user)
            db.session.commit()
            flash('Registration Successful')
            return redirect(url_for('login'))
        except IntegrityError:
            # Placeholder expection error, so the thing does not crap itself
            db.session.rollback()
            flash('user already exists')

    return render_template('register.html', form=reg_form)


    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('vul_scanner_test_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            #forgot what this exactly does...I think it sends you to the page you wanted to view if you weren't
            #logged in,  
            next_page = url_for('home_page')
        return redirect(next_page)
    else:
        print("Form validation failed:", form.errors)
    return render_template('login.html', title='login page', form=form)

@app.route('/vul_scanner_test_page', methods=['GET', 'POST'])
def vul_scanner_test_page():
    if request.method == 'POST':
        url = request.form.get('url')
        scanner = Scanner(url)

        if not url:
            flash('Enter URL first!')
            return render_template('vul_scanner_test_page.html')

        if not scanner.validateUrl():
            flash('Invalid URL format!')
            return render_template('vul_scanner_test_page.html')

        try:
            scan_results = scanner.scanBoth()
            return render_template('vul_scanner_test_page.html', results=scan_results)
        except Exception as e:
            flash(f'Error scanning URL: {str(e)}')
            return render_template('vul_scanner_test_page.html')

    return render_template('vul_scanner_test_page.html', results=None)


def run_scan(scanner):
    results = scanner.xssScanner()
    session['scan_results'] = results
    session['scan_complete'] = True

@app.route('/check_scan')
def check_scan():
    return jsonify({'complete': session.get('scan_complete', False), 'results': session.get('scan_results')})
@app.route('/scan_sqli', methods=['POST'])


def scan_sqli():
    url = request.form.get('url')
    scanner = Scanner(url)

    if not url or not scanner.validateUrl():
        return jsonify({'error': 'Invalid or empty URL'})

    try:
        # 🔄 Scan both SQLi and XSS
        scan_results = scanner.scanBoth()
        return jsonify({'results': scan_results})
    except Exception as e:
        return jsonify({'error': str(e)})