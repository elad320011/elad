from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import bcrypt
import os
from dotenv import load_dotenv
from flask_mail import Mail, Message

#loads environment variables from a .env file, needed for os module
load_dotenv()
app = Flask(__name__)

# Key to sign cookies, important for security 
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB configuration
client = MongoClient("mongodb://{}:{}@{}:27017".format(os.getenv("MONGO_USERNAME"),os.getenv("MONGO_PASSWORD"),os.getenv("MONGO_URI")))
db = client.get_database(os.getenv("MONGO_DB"))
users = db.users

# Flask-Mail configuration
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
mail = Mail(app)

# Define routes for the home page and about page
@app.route("/")
def default():
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return redirect(url_for('home'))
        else:
            return render_template('login.html', message='Invalid email or password.')
    else:
        return render_template("login.html")

# Register page, verification email
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        existing_user = users.find_one({'email': email})
        print (existing_user)
        if not existing_user:
            return render_template('register.html', message='A user with this email address already exists.')
        else:
            # Generate a random verification code
            code = os.urandom(16).hex()
            # Hash the password
            hashed = bcrypt.hashpw(password, bcrypt.gensalt())
            # Insert the new user into the database
            users.insert_one({'email': email, 'password': hashed, 'verified': False, 'verification_code': code})
            # Send a verification email
            msg = Message('Verify your email', recipients=[email])
            verify_url = url_for('verify', _external=True, email=email, code=code)
            msg.body = f'Click this link to verify your email: {verify_url}'
            mail.send(msg)
            return redirect(url_for('login'))
    else:
        return render_template("register.html")

# Email verify page
@app.route('/verify')
def verify():
    email = request.args.get('email')
    code = request.args.get('code')
    if not email or not code:
        return render_template('error.html', message='Invalid verification link.')
    user = users.find_one({'email': email})
    if not user:
        return render_template('error.html', message='Invalid verification link.')
    if user['verification_code'] != code:
        return render_template('error.html', message='Invalid verification code.')
    users.update_one({'email': email}, {'$unset': {'verification_code': ''}, '$set': {'verified': True}})
    return render_template('success.html', message='Your account has been successfully verified!')

# Home page
@app.route('/home')
def home():
    return render_template('home.html')

# Contact page
@app.route("/contact")
def about():
    return render_template("contact.html")

# Project page
@app.route("/project")
def project():
    return render_template("myproject.html")

# Run application
if __name__ == '__main__':
    app.run(debug=True)
