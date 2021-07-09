from models.base_model import BaseModel
import peewee as pw
from flask_login import UserMixin
import re
from werkzeug.security import generate_password_hash
from playhouse.hybrid import hybrid_property

class User(BaseModel, UserMixin):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique=True, null=False)
    password = pw.TextField(null = False)
    profile_image_path = pw.TextField(default= 'https://www.jobstreet.co.id/en/cms/employer/wp-content/plugins/all-in-one-seo-pack/images/default-user-image.png')
    
    @hybrid_property
    def full_image_path(self):
        if self.image_path:
            pass


    
    def validate(self):
        email_existing = User.get_or_none(User.email == self.email)
        if email_existing:
            self.errors.append('Username already exists!')
        
        existing_username = User.get_or_none(User.username == self.username)
        if existing_username:
            self.errors.append('Username already exists!')

        if len(self.password) <= 6:
            self.errors.append('Password should be longer that 6 characters')
        
        has_lowercase = re.search(r"[a-z]", self.password)
        has_uppercase = re.search(r"[A-Z]", self.password)
        has_special_char = re.search(r"[\[ \] \{ \} \# \% \$ \* \@]", self.password)

        if has_lowercase and has_uppercase and has_special_char:
            self.password_hash = generate_password_hash(self.password)
        else:
            self.errors.append('Password either does not have a lowercase, uppercasem or a specials character')