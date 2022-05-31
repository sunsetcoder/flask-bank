from flask import Flask
from flask import render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask import session
from models import User
from extensions import db
from validators import *
from decimal import Decimal
import sqlite3
from passlib.hash import sha256_crypt
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.secret_key = SECRET_KEY
    login_manager.init_app(app)
    db.init_app(app)
    return app

app = create_app()

with app.app_context():
    db.create_all() # create all tables if they don't already exist

@app.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        print("user is authenticated")
        return redirect(url_for('account'))
    else:
        print("user is NOT authenticated")
        return redirect(url_for('login'))

class Number():
    def __init__(self, whole, fraction):
        self.number = None
        if validNumericNoLeadingZeros(whole) and validNumericFractionTwoDigits(fraction):
            self.whole = Decimal(whole)
            self.fraction = Decimal(fraction)
            self._num = self.whole + (self.fraction/100)
            if numberInBounds(self._num):
                self.number = self._num

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    if user_id is not None:
        return User.query.get(user_id)
    return None

@app.route('/login', methods=["GET", "POST"])
def login():
    error = None  
    # Go to accounts page if user is already logged in
    if current_user.is_authenticated:
        print("current user not authenticated")
        return redirect(url_for('account'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # validate username and password using whitelist pattern:
        if validAccountNameOrPassword(username) and validAccountNameOrPassword(password):
            # check if user exists
            user = User.query.filter_by(username=username).first()
            if user:
                if user.check_password(password): # if correct password supplied
                    login_user(user)
                    return redirect(url_for('account'))
                else: # invalid password
                    error = 'Invalid username or password'
                    flash("Invalid username or password")
            else: # invalid username
                error = 'Invalid username or password'
                flash("Invalid username or password")
        else: # invalid username and/or password input
            error = 'invalid_input'
            flash('invalid_input')
    return render_template('login.html', error = error)

@app.route("/register", methods=["GET", "POST"])
def register():
    print("register")
    # if user is already logged in, redirect to account page:
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    # POST:
    if request.method == "POST":
        # get user input from form:
        username = request.form.get("username")
        password = request.form.get("password")
        balance_whole = request.form.get("balance_whole")
        balance_fraction = request.form.get("balance_fraction")
        # whitelist valid user input according to allowed pattern:
        balance = Number(balance_whole, balance_fraction).number
        if validAccountNameOrPassword(username) and validAccountNameOrPassword(password) and (balance is not None):
            # check if username already exists
            conn = sqlite3.connect('bank.db')
            c = conn.cursor()
            user = User.query.filter_by(username=username).first()
            user_exists = c.fetchone()
            conn.commit()
            # store in db if user doesn't exist:
            if user_exists is None:
                password = sha256_crypt.hash(password)
                user = User(username=username,
                                password=password, 
                                balance=balance)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash("Registration completed! Redirecting to account page...")
                return redirect(url_for("account"))
        else: 
            # if user already exists or input is invalid:
            flash('Registration failed. Invalid input')
            return redirect(url_for('register'))
    # GET:
    return render_template("register.html")

@app.route('/account', methods=["GET", "POST"])
@login_required
def account():
    return render_template("account.html")

@app.route('/withdraw', methods=["POST"])
@login_required
def withdraw():
    if request.method == 'POST':
        whole = request.form['withdraw_amount_whole']
        fraction = request.form['withdraw_amount_fraction']
        amount = Number(whole, fraction).number
        if amount is None:
            flash("invalid input")
            return redirect(url_for('account'))
        else:
            if Decimal(amount) > current_user.balance:
                flash("Withdrawal Failed! Cannot withdraw an amount greater than balance.")
            else:
                current_user.withdraw(amount)
                flash("Withdrawal successful")
            return redirect(url_for('account'))

@app.route('/deposit', methods=["POST"])
@login_required
def deposit():
    if request.method == 'POST':
        whole = request.form['deposit_amount_whole']
        fraction = request.form['deposit_amount_fraction']
        amount = Number(whole, fraction).number
        if amount is None:
            flash("invalid input")
            return redirect(url_for('account'))
        else:
            current_user.deposit(amount)
            flash("Deposit successful")
            return redirect(url_for('account'))

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.unauthorized_handler
def unauthorized():
    flash('Unauthorized access.')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='localhost', debug=False, port=4000)