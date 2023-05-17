"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.nicepng.com/png/detail/933-9332131_profile-picture-default-png.png"

class User(db.Model):
    """User"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False,)
    last_name = db.Column(db.Text,
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable = False,
                          default= DEFAULT_IMAGE_URL)
    
    posts = db.relationship('Post', backref='user')

    @property
    def full_name(self):
        """return user's full name"""

        return f"{self.first_name} {self.last_name}"
    
    

class Post(db.Model):
    """Post"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text, 
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)




def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    app.app_context().push()
