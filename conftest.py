from app import create_app, db
from config import Config
from app.models import User, CardSet, Card, UserGroup, Study
import pytest

from _datetime import date, timedelta


@pytest.fixture
def client():
    flask_app = create_app()
 
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield testing_client  # this is where the testing happens!
 
    ctx.pop()
    
@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    user1 = User(username='ben@hotmail.com')
    user1.set_password('IoTData')
    user1.is_admin = True
    user2 = User(username='harry@gmail.com')
    user2.set_password('flask')
    
    db.session.add(user1)
    db.session.add(user2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
 
    db.drop_all()
    
@pytest.fixture
def init_database2():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    user1 = User(id=1,username='ben@hotmail.com')
    user1.set_password('IoTData')
    user1.is_admin = True
    user2 = User(id=2,username='harry@gmail.com')
    user2.set_password('flask')
    
    card_1 = Card(id=1, name="Card 1", creator = user1.id)
    card_2 = Card(id=2,name="Card 2", creator= user1.id)
    
    card_set_1 = CardSet(id=1, name="Card Set 1", measure="Sensitvity", cards=[card_1], creator=user1.id)
    card_set_2 = CardSet(id=2, name="Card Set 2", measure="Cost", cards=[card_2], creator=user1.id)
    user_group_1 = UserGroup(id=1, name="User Group 1", creator_id = user1.id )
    user_group_1.users = [user2]
    
    db.session.add(card_1)
    db.session.add(card_2)
    db.session.add(card_set_1)
    db.session.add(card_set_2)
    db.session.add(user_group_1)
    db.session.commit()
    
    db.session.add(user1)
    db.session.add(user2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
 
    db.drop_all()
    
@pytest.fixture
def init_database3():
    # Create the database and the database table
    db.create_all()
 
    # Insert user data
    user1 = User(id=1,username='ben@hotmail.com')
    user1.set_password('IoTData')
    user1.is_admin = True
    user2 = User(id=2,username='harry@gmail.com')
    user2.set_password('flask')
    
    card_1 = Card(id=1, name="Card 1", creator = user1.id)
    card_2 = Card(id=2,name="Card 2", creator= user1.id)
    
    card_set_1 = CardSet(id=1, name="Card Set 1", measure="Sensitvity", cards=[card_1], creator=user1.id)
    card_set_2 = CardSet(id=2, name="Card Set 2", measure="Cost", cards=[card_2], creator=user1.id)
    user_group_1 = UserGroup(id=1, name="User Group 1", creator_id = user1.id )
    user_group_1.users = [user2]
    study = Study(id=1, name="Study 1")
    study.card_sets = [card_set_1, card_set_2]
    study.data_values = 2
    study.number_of_columns = 4
    study.number_of_rows = 3
    study.user_group_id = user_group_1.id
    study.creator = user1.id
    study.start_date = date.today()
    study.end_date = date.today()+timedelta(days=3)
    
    db.session.add(card_1)
    db.session.add(card_2)
    db.session.add(card_set_1)
    db.session.add(card_set_2)
    db.session.add(user_group_1)
    db.session.add(study)
    db.session.commit()
    
    db.session.add(user1)
    db.session.add(user2)
 
    # Commit the changes for the users
    db.session.commit()
 
    yield db  # this is where the testing happens!
 
    db.drop_all()