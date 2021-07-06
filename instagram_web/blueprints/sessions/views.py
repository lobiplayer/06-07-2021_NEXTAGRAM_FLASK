from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/', methods=['POST'])
def login():

    username = request.form['username']
    password_to_check = request.form['password']
    print(username, password_to_check)
    user = User.get_or_none(User.username == username)
    hashed_password = user.password

    print(user.username)
    
    if user and check_password_hash(hashed_password, password_to_check):
        # set the session
        session['user_id'] = user.id
    else:
        return redirect(url_for('sessions.new'))





    # if result:
    #     flash('TRUE')
    #     return redirect(url_for('sessions.new'))
    # else:
    #   return render_template('new.html', name=request.form['username'])