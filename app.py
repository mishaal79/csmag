# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
# import datetime from the dateime
from datetime import datetime
# improt flask_sqlalchemy for databases
from flask_sqlalchemy import SQLAlchemy
# import forms from the wtforms
from wtforms import Form, BooleanField, StringField, PasswordField, validators
# import flash from the flask.helpers
from flask.helpers import flash
# import LoginManager from the flask_login
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user


# create the application object
app = Flask(__name__, template_folder='templates')
# configuring databases and the relative path 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


# login
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY']='619619'

# create table with fields
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(50))
    sign_up_date = db.Column(db.DateTime, default = datetime.utcnow)
    path = db.Column(db.String(50))
    languages = db.Column(db.String(50))
    about = db.Column(db.Text())

    def __repr__(self):
       return '<Users %r>' % self.id

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# use decorators to link the function to a url
@app.route('/')
def home():
    return render_template('welcome.html')  # render a template
    
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    name = None
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        user = User.query.filter_by(username=user_username).first()
        try:
            name = user_username
            login_user(user)
            return redirect('/profile')
        except:
            error = "The user does not exist, please sign up for an account"
    return render_template('login.html', error=error)

# Route for handling the signup page logic
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    error = None
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        user_email = request.form['email']
        new_user = User(username=user_username,password=user_password,email=user_email)   
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            if not user_username:
                error = 'Username is required.'
            elif not user_password:
                error = 'Password is required.'
            elif not user_email:
                error = 'Email address is required.'
            else:
                error = "This username is alredy taken"       
    return render_template('signup.html', error=error)

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    error = None
    try:
        user_username = current_user.username
        user = User.query.filter_by(username=user_username).first()
    except:
        error = "Please Log In or Sign Up!"
        render_template("profile.html", error=error)
    if request.method == 'POST':
        user_path = request.form['path']
        user_about = (request.form['about']).strip()
        languages = request.form.getlist('languages')
        user_languages =  ",".join(languages)
        user.path = user_path
        user.languages = user_languages
        user.about = user_about
        try:
            db.session.commit()
            return redirect('/profile')
        except:
            if not user_username:
                error = 'Username is required.'
            elif not user_path:
                error = 'A career path is required.'
            elif not user_languages:
                error = 'A preferred language is required'
            elif not user_about:
                error = 'An about bio is required'
    return render_template("profile.html", error=error)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
    
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
