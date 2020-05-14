# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request
# import datetime from the dateime
from datetime import datetime
# improt flask_sqlalchemy for databases
from flask_sqlalchemy import SQLAlchemy

# create the application object
app = Flask(__name__)
# configuring databases and the relative path 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# create table with fields
class SignUp(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(50))
    sign_up_date = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
       return '<Users %r>' % self.id

# use decorators to link the function to a url
@app.route('/')
def home():
    return "Hello, World!"  # return a string


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# Route for handling the signup page logic
@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    error = None
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        user_email = request.form['email']
        new_user = SignUp(username=user_username,password=user_password,email=user_email)   
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return "Change to to check if the username is alredy taken"       
    return render_template('signup.html', error=error)

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    return render_template("profile.html")
    
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
