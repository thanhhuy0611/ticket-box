from flask_login import UserMixin
from src import db
from werkzeug.security import check_password_hash, generate_password_hash

#DEFINING MODELS
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(200),nullable= False)
    body =  db.Column(db.String,nullable= False)
    author = db.Column(db.String,nullable = False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    user_id = db.Column(db.String,nullable = False)
    view_count = db.Column(db.Integer, default=0)


class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    email = db.Column(db.String,nullable= False,unique = True)
    password = db.Column(db.String,nullable = False,unique = False)
    user_name =  db.Column(db.String,nullable= False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password,password)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body =  db.Column(db.String,nullable= False)  
    user_id = db.Column(db.Integer,nullable = False)
    blog_id = db.Column(db.Integer,nullable = False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())


db.create_all()