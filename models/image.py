from models.base_model import BaseModel
import peewee as pw
from models.user import User

class Image(BaseModel):
    image_url = pw.TextField(null = False)
    user = pw.ForeignKeyField(User, backref='images', on_delete='CASCADE')
    image_caption = pw.TextField(null = True)
    image_hashtags = pw.TextField(null = True)
    
