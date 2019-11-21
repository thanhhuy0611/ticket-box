from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, validators, PasswordField, SubmitField


app = Flask(__name__, static_folder='static')
app.config.from_object('config.Config')

#config SQLAlchemy
db = SQLAlchemy(app)

#-------------------------------------------------
##  import models
from src.models.user import Users, Blog, Comment
from src.components.user import *

migrate = Migrate(app, db)
## set up flask-login
login_manager= LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login"
# set current_user
@login_manager.user_loader
def load_user(id):
  return Users.query.filter_by(id = b).first()

#-------------------------------------------------------
## import controlers file
from src.components.user import user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')

# set current_user
@login_manager.user_loader
def load_user(b):
    return Users.query.filter_by(id = b).first()

# show all blog
@app.route('/',methods=["GET","POST"])
def home():
    posts = Blog.query.all()
    filter = request.args.get('filter')
    for post in posts:
        post.comments = Comment.query.filter_by(blog_id = post.id).all()
    if filter == 'most-recently':
        posts = Blog.query.order_by(Blog.created_on.desc()).all()
    if filter == 'top-viewed':
        posts = Blog.query.order_by(Blog.view_count.desc()).all()
    return render_template('/index.html',posts = posts, ref = 'home')

# sign up account
@app.route('/signup', methods=["GET","POST"])
def sign_up():
    form = RegisterForm()
    if not current_user.is_anonymous:
        return redirect(url_for('home'))
    if request.method == "POST":
        if form.validate_on_submit():
        #check email unique
            is_email_exits = Users.query.filter_by(email = form.email.data).first()
            print("emailcheck",is_email_exits)
            if is_email_exits:
                flash('Email is exits. Please try again!','danger')
            if not is_email_exits:
                new_user =  Users(
                    email = form.email.data,        
                    user_name = form.username.data
                )
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('home'))
        else:
            for field,error in form.errors.items():
                flash(f'{field}: {error[0]}','danger')
    return render_template('/signup.html', form = form)


# add new blog
@app.route('/newpost',methods=["GET","POST"])
def new_post():
    if request.method == "POST":
        new_blog =  Blog(
            title = request.form["title"],
            body = request.form["body"],
            author = current_user.user_name,
            user_id = current_user.id
        )
        db.session.add(new_blog)
        db.session.commit()
        return redirect(url_for('home'))

# delete a blog
@app.route('/blog/<b>', methods=["GET","POST","DELETE"])
@login_required
def delete_blog(b):
    if request.method =="POST":
        post = Blog.query.filter_by(id = b).first()
        if not post:
            return "there is no such post"
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('home'))


# check account login
@app.route('/login', methods=["GET","POST"])
def login():
    if not current_user.is_anonymous:
        return redirect(url_for('home'))

    if request.method == "POST":
        user = Users.query.filter_by(email = request.form["email"]).first()
        if not user:
            flash('Email incorrect!','danger')
        if user:
            if user.check_password(request.form['password']):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Password incorrect!','danger')
    return render_template('/login.html')

# logout 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

