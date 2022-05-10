from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from extensions import db
from decimal import Decimal

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(127), unique=True)
    password = db.Column(db.String(127))
    balance = db.Column(db.Numeric(), nullable=False)
 
    def set_password(self,password):
        self.password = password
     
    def check_password(self,password):
        return self.password == password
    
    def deposit(self, amount):
        amount = Decimal(amount)
        self.balance += amount
        db.session.commit()
    
    def withdraw(self, amount):
        amount = Decimal(amount)
        self.balance -= amount
        db.session.commit()