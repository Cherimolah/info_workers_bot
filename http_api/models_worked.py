from loader import app
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)
1

class item(db.Model):
    id = db.Column(db.integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    count = db.Column(db.integer, default=0)

    def __init__(self, name, position):
        self.name = name
        self.count = count

db.create_all()

class user(db.Model):
    user_id = db.Column(db.integer, primary_key=True)
    screen_name = db.Column(db.String)
    Full_name = db.Column(db.String)

    def __init__(self, user_id, screen_name, Full_name):
        self.user_id = user_id
        self.screen_name = screen_name
        self.Full_name = Full_name

db.create_all()

class history(db.Model):
    id = db.Column(db.integer, primary_key=True)
    user_id = db.Column(db.integer, foreign(user.user_id))
    item_id = db.Column(db.integer, foreign(item_id))
    alteration = db.Column(db.integer)
    created_at = db.Column(datetime)

    def __init__(self, user_id, item_id, alteration, reated_at):
        self.user_id = user_id
        self.item_id = item_id
        self.alteration = alteration
        self.created_at = created_at

db.create_all()