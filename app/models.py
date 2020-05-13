from flask_login import UserMixin
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))
    type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "employee",
        "polymorphic_on": type,
    }

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Participant(User):
    email = db.Column(db.String(320))

    gender = db.Column(db.String(10))
    age_group = db.Column(db.String(10))
    country_of_birth = db.Column(db.String(100))
    education_level = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    latest_country = db.Column(db.String(100))
    income = db.Column(db.String(100))

    completed_form = db.Column(db.Boolean, default=False)
    completed_study = db.Column(db.Boolean, default=False)

    user_group_id = db.Column("UserGroup", db.ForeignKey("user_group.id"))
    user_group = db.relationship(
        "UserGroup",
        foreign_keys=[user_group_id],
        backref=backref("users", cascade="all,delete"),
    )

    __mapper_args__ = {"polymorphic_identity": "participant"}


class Admin(User):
    cards = db.relationship("Card", backref="creator")
    data_value_labels = db.relationship("DataValueLabel", backref="creator")
    studies = db.relationship("Study", backref="creator")
    card_sets = db.relationship("CardSet", backref="creator")

    __mapper_args__ = {"polymorphic_identity": "admin"}


class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    creator_id = db.Column("Admin", db.ForeignKey("user.id"))

    creator = db.relationship(
        "Admin", foreign_keys=[creator_id], backref="user_groups"
    )
    study = db.relationship(
        "Study",
        uselist=False,
        backref=backref("user_group", cascade="all,delete"),
    )

    def __repr__(self):
        return str(self.name)


class DataValueLabel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(500))

    study_id = db.Column("Study", db.ForeignKey("study.id"))
    creator_id = db.Column("Admin", db.ForeignKey("user.id"))

    data_values = db.relationship("DataValue", backref="data_value_label")


class Study(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))
    data_values = db.Column(db.Integer)
    number_of_columns = db.Column(db.Integer)
    number_of_rows = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    mail_sent = db.Column(db.Boolean, default=False)

    card_set_x_id = db.Column(db.Integer, db.ForeignKey("card_set.id"))
    card_set_y_id = db.Column(db.Integer, db.ForeignKey("card_set.id"))
    creator_id = db.Column("Admin", db.ForeignKey("user.id"))
    user_group_id = db.Column(db.Integer, db.ForeignKey("user_group.id"))

    card_set_x = db.relationship(
        "CardSet", foreign_keys=card_set_x_id, backref="studies_x"
    )
    card_set_y = db.relationship(
        "CardSet", foreign_keys=card_set_y_id, backref="studies_y"
    )
    data_value_labels = db.relationship(
        "DataValueLabel", backref="study", cascade="all, delete"
    )
    responses = db.relationship(
        "Response", backref="study", cascade="all, delete"
    )
    
    
    def __repr__(self):
        return str(self.name)


class CardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    measure = db.Column(db.String(100))

    creator_id = db.Column("Admin", db.ForeignKey("user.id"))

    cards = db.relationship("Card", backref="card_set", cascade="all, delete")

    def __repr__(self):
        return str(self.name)


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    image = db.Column(db.String(100))

    creator_id = db.Column("Admin", db.ForeignKey("user.id"))
    card_set_id = db.Column(db.Integer, db.ForeignKey("card_set.id"))

    positions = db.relationship("CardPosition", backref='card')
    
    def __repr__(self):
        return str(self.name)


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    study_id = db.Column("Study", db.ForeignKey("study.id"))
    participant_id = db.Column("Participant", db.ForeignKey("user.id"))
    
    card_positions = db.relationship('CardPosition', backref='response')
    data_values = db.relationship('DataValue', backref='response')
    participant = db.relationship(
        "Participant", foreign_keys=participant_id, backref="response"
    )
    
    
class CardPosition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    
    card_id = db.Column("Card", db.ForeignKey("card.id"))
    response_id = db.Column("Response", db.ForeignKey("response.id"))
    

class DataValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    column = db.Column(db.Integer)
    row = db.Column(db.Integer)
    value = db.Column(db.Integer)  

    data_value_label_id = db.Column("DataValueLabel", db.ForeignKey("data_value_label.id"))
    response_id = db.Column("Response", db.ForeignKey("response.id"))

    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
