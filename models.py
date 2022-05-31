from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from extensions import db
from decimal import Decimal
from passlib.hash import sha256_crypt

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True)
    password = db.Column(db.String())
    balance = db.Column(db.Numeric(), nullable=False)
 
    def set_password(self,password):
        self.password = sha256_crypt.hash(password)
     
    def check_password(self,password):
        return sha256_crypt.verify(password, self.password)
    
    def deposit(self, amount):
        amount = Decimal(amount)
        self.balance += amount
        db.session.commit()
    
    def withdraw(self, amount):
        amount = Decimal(amount)
        self.balance -= amount
        db.session.commit()