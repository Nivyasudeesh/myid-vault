from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Identity

app = Flask(__name__)
app.secret_key = 'supersecret'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myid.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/dashboard')
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            return "Username already exists"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    identity = Identity.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        if identity:
            db.session.delete(identity)
            db.session.commit()
        identity = Identity(
            user_id=current_user.id,
            name=request.form['name'],
            age=request.form['age'],
            email=request.form['email'],
            college=request.form['college'],
            student_id=request.form['student_id']
        )
        db.session.add(identity)
        db.session.commit()
        return redirect('/share')
    return render_template('dashboard.html', data=identity)

@app.route('/share', methods=['GET', 'POST'])
@login_required
def share():
    identity = Identity.query.filter_by(user_id=current_user.id).first()
    if not identity:
        return redirect('/dashboard')
    if request.method == 'POST':
        selected = request.form.getlist('fields')
        shared = {k: getattr(identity, k) for k in selected}
        return render_template('result.html', shared=shared)
    return render_template('share.html', data=identity)
