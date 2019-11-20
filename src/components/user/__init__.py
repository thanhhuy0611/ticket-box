from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from wtforms import StringField, validators, PasswordField, SubmitField


user_blueprint = Blueprint('post', __name__, template_folder='../../templates')

## My awesome forms
class RegisterForm(FlaskForm):
    username = StringField(
        "User name", validators=[
            validators.DataRequired(), 
            validators.Length(min=3,max=20,message="Need to be in between 3 and 20")
    ])
    email = StringField(
        "Email", validators=[
            validators.DataRequired(), 
            validators.Length(min=3,max=200,message="Need to be in between 3 and 20"), 
            validators.Email("Please enter correct email!")
    ])
    password = PasswordField(
        'Password', validators=[
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm password', validators=[validators.DataRequired()])
    submit = SubmitField('Sign up')


from src.models.user import Users, Blog, Comment
from src import db

# comment
@user_blueprint.route('/<id>/comments', methods=['GET','POST'])
def create_comment(id):
    ref = request.args.get('ref')
    print(ref)
    if request.method == "POST":
        comment = Comment(
            body = request.form["body"],
            user_id = current_user.id,
            blog_id = id
        )
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for(ref, id= id))

# delete comment
@user_blueprint.route('/<id>/comments/<id_comment>', methods=['GET','POST'])
def delete_comment(id,id_comment):
    ref = request.args.get('ref')
    print('ref',ref)
    comment = Comment.query.filter_by(id = id_comment).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for(ref, id= id))


#view a blog
@user_blueprint.route('/<id>',methods=["GET","POST"])
def view_post(id):
    post = Blog.query.get(id)
    post.view_count +=1
    db.session.commit() 
    post.comments = Comment.query.filter_by(blog_id = id).all()
    return render_template('/post.html',post = post, ref = 'post.view_post')

#Edit a blog
@user_blueprint.route('/<id>/edit',methods=['GET','POST'])
def edit_post(id):
    post = Blog.query.get(id)
    if request.method == "POST":
        post.title = request.form['title']
        post.body = request.form['body']
        db.session.commit()
        return redirect(url_for('post.view_post',id = id))
    return render_template('/editpost.html',post = post)



