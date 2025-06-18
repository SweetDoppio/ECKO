from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask import render_template, flash, redirect, url_for, request, session, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import db, app
from app.forms import LoginForm, RegisterForm
from app.models import User, Post
from app.scanner import Scanner
from app.scanner import Scanner
import sqlalchemy as sa
from urllib.parse import urlsplit
from bokeh.plotting import figure
from bokeh.embed import components
import threading
import threading
from random import randint
import time
from sqlalchemy.exc import IntegrityError
import time
from sqlalchemy.exc import IntegrityError

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


#below functions are for visual indicators that the scanning is being run,


@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')
    scanner = Scanner(url)
    
    if not url:
        return jsonify({'error': 'Enter URL first!'})
        
    if not scanner.validateUrl():
        return jsonify({'error': 'Invalid URL format!'})

    try:
        results = scanner.scanXss()
        return jsonify({
            'status': 'complete',
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/start_scan', methods=['POST'])
def start_scan():
    url = request.form.get('url')
    session['scan_complete'] = False
    scanner = Scanner(url)
    thread = threading.Thread(target=run_scan, args=(scanner, ))
    thread.start()

    return jsonify({'status: Scan started'})

def run_scan(scanner):
    results = scanner.xssScanner()
    session['scan_results'] = results
    session['scan_complete'] = True

@app.route('/check_scan')
def check_scan():
    return jsonify({'complete': session.get('scan_complete', False), 'results': session.get('scan_results')})

@app.route('/sxx_scanner_test_page', methods=['GET', 'POST'])
def sxx_scanner_test_page():
    
    if request.method == 'POST':    
        url = request.form.get('url')
        scanner = Scanner(url)

        if not url:
            flash('Enter url first!')
            return render_template('sxx_scanner_test_page.html')
        if not scanner.validateUrl():
            #Should return necessary flash messages from route.py...
            return render_template('sxx_scanner_test_page.html')

        try:
            scan_results = scanner.scanXss()
            return render_template('sxx_scanner_test_page.html', results=scan_results)
        
        except request.exceptions.RequestException as e:
            #Handles any errors without giving the user a big error page 
            flash(f'Error scanning URL: {str(e)}')
            return render_template('sxx_scanner_test_page.html')
    return render_template('sxx_scanner_test_page.html', results= None)
#below functions are for visual indicators that the scanning is being run,


@app.route('/scan', methods=['POST'])
def scan():
    url = request.form.get('url')
    scanner = Scanner(url)
    
    if not url:
        return jsonify({'error': 'Enter URL first!'})
        
    if not scanner.validateUrl():
        return jsonify({'error': 'Invalid URL format!'})

    try:
        results = scanner.scanXss()
        return jsonify({
            'status': 'complete',
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)})
    

@app.route('/start_scan', methods=['POST'])
def start_scan():
    url = request.form.get('url')
    session['scan_complete'] = False
    scanner = Scanner(url)
    thread = threading.Thread(target=run_scan, args=(scanner, ))
    thread.start()

    return jsonify({'status: Scan started'})

def run_scan(scanner):
    results = scanner.xssScanner()
    session['scan_results'] = results
    session['scan_complete'] = True

@app.route('/check_scan')
def check_scan():
    return jsonify({'complete': session.get('scan_complete', False), 'results': session.get('scan_results')})

@app.route('/sxx_scanner_test_page', methods=['GET', 'POST'])
def sxx_scanner_test_page():
    
    if request.method == 'POST':    
        url = request.form.get('url')
        scanner = Scanner(url)

        if not url:
            flash('Enter url first!')
            return render_template('sxx_scanner_test_page.html')
        if not scanner.validateUrl():
            #Should return necessary flash messages from route.py...
            return render_template('sxx_scanner_test_page.html')

        try:
            scan_results = scanner.scanXss()
            return render_template('sxx_scanner_test_page.html', results=scan_results)
        
        except request.exceptions.RequestException as e:
            #Handles any errors without giving the user a big error page 
            flash(f'Error scanning URL: {str(e)}')
            return render_template('sxx_scanner_test_page.html')
    return render_template('sxx_scanner_test_page.html', results= None)


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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/register',  methods=['GET', 'POST'])
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
            #forgot what this exactly does...I think it sends you to the page you wanted to view if you weren't
            #logged in,  
            next_page = url_for('index')
        return redirect(next_page)
    else:
        print("Form validation failed:", form.errors)
    return render_template('login.html', title='login page', form=form)

