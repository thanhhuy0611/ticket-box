from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from src.models.user import User
event_blueprint = Blueprint('event', __name__, template_folder='../../templates')

## 'host/event/'
@event_blueprint.route('/')
@login_required
def root():
  user = User.query.get(1)
  return "USER"
