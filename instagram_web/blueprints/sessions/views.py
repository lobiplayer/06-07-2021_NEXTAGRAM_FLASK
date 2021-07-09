from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

sessions_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

@sessions_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/logoutpage', methods=['GET'])
def logoutpage():
    return render_template('sessions/logoutpage.html')

@sessions_blueprint.route('/', methods=['POST'])
def login():

    username = request.form['username']
    password_to_check = request.form['password']
    print(username, password_to_check)
    user = User.get_or_none(User.username == username)
    
    if not user: #check if user the username exists in the database. If not, the users will be directed to the login page
        flash('Wrong login credentials')
        return redirect(url_for('sessions.new'))
    else:
        hashed_password = user.password

    print(user.username)
    
    if user and check_password_hash(hashed_password, password_to_check):
        # set the session
        # session['user_id'] = user.id #this was used for sessions login. Now commented because flash login being used.
        login_user(user)
        flash('Login successfull')
        return redirect(url_for('users.show', username = user.username))
    else:
        flash('Wrong login credentials')
        return redirect(url_for('sessions.new'))

@sessions_blueprint.route('/logout', methods=['POST'])
def logout():
    # remove the username from the session if it's there
    # session.pop('username', None) # this was used with sessions logout, now using flash logout on the next line.
    logout_user()
    flash('Signed out')
    return redirect(url_for('sessions.new'))
