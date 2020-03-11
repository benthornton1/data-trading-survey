from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), index=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    
    gender = db.Column(db.String(10))
    age_group = db.Column(db.String(10))
    country_of_birth = db.Column(db.String(100))
    education_level = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    country_born = db.Column(db.String(100))
    latest_country = db.Column(db.String(100))
    income = db.Column(db.String(100))
    completed_form = db.Column(db.Boolean, default=False)

    completed_study = db.Column(db.Boolean, default=False)
    
    user_group_id = db.Column('UserGroup', db.ForeignKey('user_group.id'))
    user_group_owner = db.relationship('UserGroup', foreign_keys='UserGroup.creator_id', backref="created_by", lazy="dynamic")
    card_owner = db.relationship('Card', backref='owner', lazy='dynamic')
    
    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users = db.relationship('User',foreign_keys='User.user_group_id', backref='user_group', lazy='dynamic')
    study = db.relationship('Study', uselist=False, backref="user_group")
    creator_id = db.Column('User', db.ForeignKey('user.id'))
    
    def __repr__(self):
        return str(self.name)
    
card_sets = db.Table('card_sets',
                 db.Column('card_set_id', db.Integer, db.ForeignKey('card_set.id'), primary_key=True),
                 db.Column('study_id', db.Integer, db.ForeignKey('study.id'), primary_key=True))

class DataValuesLabels(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(500))
    study_id = db.Column('Study', db.ForeignKey('study.id'))
    
class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    desc = db.Column(db.String(100))
    image = db.Column(db.String(100))
    card_sets = db.relationship('CardSet', secondary=card_sets, backref=db.backref('studies', lazy='dynamic',  cascade="all,delete"))
    data_values = db.Column(db.Integer)
    data_values_labels = db.relationship('DataValuesLabels', backref='study')
    number_of_columns = db.Column(db.Integer)
    number_of_rows = db.Column(db.Integer)
    user_group_id = db.Column(db.Integer, db.ForeignKey('user_group.id'))
    creator = db.Column('User', db.ForeignKey('user.id'))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    mail_sent = db.Column(db.Boolean)
    
    def __repr__(self):
        return str(self.name)

cards = db.Table('cards',
                 db.Column('card_id', db.Integer, db.ForeignKey('card.id', ondelete="CASCADE"), primary_key=True),
                 db.Column('card_set_id', db.Integer, db.ForeignKey('card_set.id', ondelete="CASCADE"), primary_key=True))
     
class CardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    measure = db.Column(db.String(100))
    cards = db.relationship('Card', secondary=cards, backref=db.backref('card_sets', lazy='dynamic',  cascade="all,delete"))
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return str(self.name)
    
    
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    desc = db.Column(db.String(500))
    image = db.Column(db.String(100))

    creator = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return str(self.name)
    
    
class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column('User', db.ForeignKey('user.id'))
    study = db.Column('Study', db.ForeignKey('study.id'))
    cards_x = db.Column(db.JSON)
    cards_y = db.Column(db.JSON)
    data_values = db.Column(db.JSON)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))