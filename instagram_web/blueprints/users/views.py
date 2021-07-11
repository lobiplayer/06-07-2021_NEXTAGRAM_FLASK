from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user
from instagram_web.util.helpers import upload_file_to_s3
from app import app


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
      return render_template('sessions/new.html', username = user.username)
    else:
      return render_template('users/new.html', name=request.form['username'])


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    if user:
        return render_template('users/show.html', user = user)
    else:
        flash('no such user found')
        return redirect(url_for('home'))


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    user = User.get_or_none(User.id == id)
    return render_template('users/edit.html', user = user)



@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    user = User.get_or_none(User.id == id)

    if user:
        if current_user.id == int(id):
            params = request.form
            
            user.username = params.get('username')
            user.email = params.get('email')

            # password = params.get('password')

            if user.save():
                flash('Details have been updated succesfully!')
                return redirect(url_for('users.show', username = user.username))
            else:
                flash('Something went wrong')
                return redirect(url_for('users.show', username = user.username))


@users_blueprint.route('/<id>/updatepassword', methods=['POST'])
def updatepassword(id):
    user = User.get_or_none(User.id == id)

    if user:
        if current_user.id == int(id):
            params = request.form
 
            password = params.get('password')
            print(password)
            hashed_password = generate_password_hash(password)
            user.password = hashed_password
            
            if  user.save():
                flash('Password has been succesfully updated!')
                return redirect(url_for('users.show', username = user.username))
            else:
                flash('Something went wrong')
                return redirect(url_for('users.show', username = user.username))


@users_blueprint.route('/<id>/upload', methods=['POST'])
def upload(id):

    user = User.get_or_none(User.id == id)

    if user:
        if current_user.id == int(id):

    
            if 'user_file' not in request.files:
                return "No user_file key in request.files"
            
            file = request.files['user_file']

            print(file.content_type)

            if file.filename == "":
                return "Please select a file"
            
            file.filename = secure_filename(file.filename)
            image_path   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])


            print(user.username, user.id, user.email, user.profile_image_path)
            user.profile_image_path = image_path
            print(user.username, user.id, user.email, user.profile_image_path)

            if user.save():
                return redirect(url_for('users.show', username = user.username))
            else:
                flash('image upload failed')
                return redirect(url_for('users.show', username = user.username))
        
        else:
            flash('Hey, change your own profile!')
            return redirect(url_for('users.show', username = user.username))
    
    else:
        flash('Username not found')
        return redirect(url_for('home'))




# @users_blueprint.route('<id>/profile', methods=['GET'])
# def profile():
#     if session.get('user_id'):
#         # use the sessions's user_id value ste via login

#         user = User.get_or_none(User.id == session['user_id'])
#         if user:
#             username = user.username
#         else:
#             username = None
#         return render_template('users/profile.html', username = username)
#     else:
#         return redirect(url_for('sessions.new'))