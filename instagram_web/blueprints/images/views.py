from flask import Blueprint, render_template, redirect, request, flash
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from models.image import Image
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import app
from flask_login import current_user
from models.image import Image
from models.user import User

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')


@images_blueprint.route('/new')
def new():
    return render_template('images/new.html')

@images_blueprint.route('/show', methods=["GET"])
def show():
    images = Image.select()
    users = User.select()
    
    for image in images:
        print(image.image_url)

    if images:
        return render_template('images/show.html', images = images, users= users)
    else:
        flash('Sorry, now pictures to show')
        return redirect(url_for('home'))

@images_blueprint.route('/', methods=["POST"])
def create():
    if 'user_file' not in request.files:
        return 'no file found'

    file = request.files['user_file']

    file.filename = secure_filename(file.filename)

    #save image to S3 and get path
    image_path = upload_file_to_s3(file, app.config["S3_BUCKET"])

    print(image_path)

    caption = request.form['caption'] 
    hashtags = request.form['hashtags']
    print(hashtags)

    #save image object to database

    image = Image(image_url=image_path, user_id=current_user.id, image_caption=caption, image_hashtags=hashtags)

    print('!!!', image.image_hashtags)
    if image.save():
        flash('Image succesfully saved')
        return redirect(url_for('users.show', username= current_user.username))
    else:
        flash('Upload failed')
        return render_template('images/new.html')
    return render_template('images/new.html')
