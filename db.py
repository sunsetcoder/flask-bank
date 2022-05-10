from flask_sqlalchemy import SQLAlchemy

# https://www.askpython.com/python-modules/flask/flask-user-authentication
# https://dev.to/sm0ke/flask-cheat-sheet-and-free-samples-25im

db = SQLAlchemy()

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String())
    balance = db.Column(db.Numeric(), nullabe=False)
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

class Transaction(db.Model):
    pass

    def __repr__(self):
        return "transaction"