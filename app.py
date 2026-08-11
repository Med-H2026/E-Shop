from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user,current_user, login_required
from models import db,User
from forms import SignupForm,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # where to redirect if not logged in

app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/products')
def products():
    return '<h1>Products Page</h1>'

@app.route('/contact')
def contact():
    return '<h1>Contact Page</h1>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('Logged in successfully!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check email and password', 'danger')
            
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))   

@app.route('/signup',methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit(): # runs only when user click submit and form is valid
        hashed_pw = generate_password_hash(form.password.data) # don't save plain password
        user = User(username=form.username.data,email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now login.', category='success')
        return redirect(url_for('login'))
    if form.errors:
        print(form.errors)
    return render_template('signup.html',form =form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
