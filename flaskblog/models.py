from datetime import  datetime
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique= True, nullable=False)
    email = db.Column(db.String(255), unique= True, nullable=False)
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    password = db.Column(db.String(255), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    def __json__(self):
        return {'username': self.username, 'email': self.email, 'image': self.image_file}
    for_json = __json__  # supported by simplejson

    '''@classmethod
    def from_json(cls, json):
        obj = cls()
        obj.a = json['username']
        obj.b = json['email']
        obj.c = json['image']
        return obj'''

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

    def __json__(self):
        return {'title': self.title, 'date_posted': self.date_posted.timestamp()}

    for_json = __json__  # supported by simplejson


