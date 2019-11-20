from flask import Blueprint, render_template

user_blueprint = Blueprint('userbp', __name__, template_folder='../../templates')

## 'host/user/'
@user_blueprint.route('/')
def root():
  return render_template('user/index.html')

@user_blueprint.route('/login')
def login():
  return "LOGIN PAGE"