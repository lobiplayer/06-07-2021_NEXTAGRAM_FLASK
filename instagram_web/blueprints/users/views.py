from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import generate_password_hash


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():

    username = request.form['username'] 
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)
    user = User(username= username, email= email, password=hashed_password)

    if user.save():
      flash('User has successfully been created')
      return redirect(url_for('users.new'))
    else:
      return render_template('users.new.html', name=request.form['username'])


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass

@users_blueprint.route('/profile')
def profile():
    if session.get('user_id'):
        # use the sessions's user_id value ste via login

        user = User.get_or_none(User.id == session['user_id'])
        if user:
            username = user.username
        else:
            username = None
        return render_template('users/profile.html', username = username)
    else:
        return redirect(url_for('sessions.new'))