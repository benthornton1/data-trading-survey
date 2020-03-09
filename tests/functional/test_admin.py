from app import db
from app.models import Card, CardSet, User, UserGroup, Study
from flask_login import current_user
from _datetime import date, timedelta
from flask import url_for

from app.admin.forms import UserForm, CardForm, CardSetForm, UserGroupForm

def login_admin(client, username, password):
    return client.post('/auth/login',
                            data=dict(username=username, password=password),
                            follow_redirects=True)
def create_study(client):
    card_set_1 = CardSet.query.filter_by(id=1).first()
    card_set_2 = CardSet.query.filter_by(id=2).first()
    user_group_1 = UserGroup.query.filter_by(id=1).first()
            
    data = dict(
        name = 'Test Study 1',
        cards_set_1 = card_set_1.id,
        cards_set_2 = card_set_2.id,
        data_values = 1,
        number_of_rows = 3,
        number_of_columns = 4,
        user_group = user_group_1.id,
        start_date = date.today(),
        end_date = date.today()+timedelta(days=3)
    )
    
    url = client.get('/admin/new_study')
    assert url.location=='http://localhost/admin/edit_study/1'
    # return client.post(url_for('admin.edit_study', study_id=1),
    #                     data=data,
    #                     follow_redirects=True)
    return client.post('/admin/edit_study/1',
                        data=data,
                        follow_redirects=True)

def test_create_study_model(client, init_database2):
    with client:
        user = login_admin(client, 'ben@hotmail.com', 'IoTData')

        card_set_1 = CardSet.query.filter_by(id=1).first()
        card_set_2 = CardSet.query.filter_by(id=2).first()
        user_group_1 = UserGroup.query.filter_by(id=1).first()
        
        study = Study(id=1,
                    name="Study 1",
                    card_sets = [card_set_1, card_set_2],
                    data_values = 2,
                    number_of_columns = 3,
                    number_of_rows = 4,
                    user_group_id = user_group_1.id,
                    creator = current_user.id,
                    start_date = date.today(),
                    end_date = date.today()+timedelta(days=3)
        )
        
        db.session.add(study)
        db.session.commit()
        assert Study.query.filter_by(id=1).first() is not None
        response = client.get('/admin')
        assert b'Study 1' in response.data
        
        
        
        

def test_create_study_form(client, init_database2):
    # with client:
    
    user = login_admin(client, 'ben@hotmail.com', 'IoTData')
    response = create_study(client)
    assert b'Test Study 1' in response.data
    assert b'Card Set 1' in response.data
    assert b'Card Set 2' in response.data
    assert b'User Group 1' in response.data

def test_delete_study(client, init_database2):
    
    user = login_admin(client, 'ben@hotmail.com', 'IoTData')
    create_study(client)
    response = client.get('/admin/delete/study/1')
    assert b'Test Study 1' not in response.data


def test_card_model(client, init_database):
    with client:
        user = login_admin(client, 'ben@hotmail.com', 'IoTData')

        card = Card(name="Card 1", creator=current_user.id)
        db.session.add(card)
        db.session.commit()
        query = Card.query.filter_by(name="Card 1", creator=current_user.id).first()
        assert query is not None
        
def test_card_set_form(client, init_database):
    with client:
        user = login_admin(client, 'ben@hotmail.com', 'IoTData')
        response = client.get('/admin/new_card_set')
        
        card_data = dict(
            card_name = "Card 1",
            image = "image"
        )
        data = dict(
            card_set_name = "Card Set 1",
            cards = card_data,
            measure = "Sensitivity",
        )
        
        
        response = client.post('/admin/card_set/1',
                               data=data,
                               follow_redirects=True)
        assert b'Card Set 1' in response.data
        
        
def test_card_set_model(client, init_database):
    with client:
        user = login_admin(client, 'ben@hotmail.com', 'IoTData')

        card_1 = Card(name="Card 1", creator=current_user.id)
        card_2 = Card(name="Card 2", creator=current_user.id)
        card_set = CardSet(name="Card Set 1", measure="Sensitivity", cards=[card_1, card_2],creator=current_user.id)

        db.session.add(card_1)
        db.session.add(card_2)
        db.session.add(card_set)
        db.session.commit()
        query = CardSet.query.filter_by(name="Card Set 1", measure="Sensitivity").first()
        assert query is not None
    
def test_delete_card_set(client, init_database2):
    
    user = login_admin(client, 'ben@hotmail.com', 'IoTData')
    card_set = CardSet.query.filter_by(id=1).first()
    response = client.get('/admin/delete/card_set/'+str(card_set.id))
    assert b'Card Set 1' not in response.data
    
def test_user_group_model(client, init_database2):
    user = login_admin(client, 'ben@hotmail.com', 'IoTData')
    
    client.get('/admin/new_user_group')
    # user_form = UserForm()
    # user_form.email.data = "test@gmail.com"
    # user_group_form = UserGroupForm()
    # user_group_form.name.data = "User Group 1"
    # user_group_form.users.data = {
    #     "emails-0-email":"test@gmail.com"
    # }
    # user_group_form.submit.data = True
    
    # user1 = dict(
    #     email = 'test@gmail.com'
    # )
    # user2 = dict(
    #     email = 'test2@gmail.com'
    # )
    data = dict(
        name = "User Group 1",
        users =  [{
            "users-1-email":"test@gmail.com"
            }],
        submit = True
    )
    

    
    response = client.post('/admin/user_group/1',
                data = data,
                follow_redirects = True)
    
    assert b'User Group 1' in response.data
    
    check_user = User.query.filter_by(username="test@gmail.com").first()
    
    assert check_user is not None
        

def test_delete_user_group(client, init_database2):
    
    user = login_admin(client, 'ben@hotmail.com', 'IoTData')
    user_group = UserGroup.query.filter_by(id=1).first()
    response = client.get('/admin/delete/user_group/'+str(user_group.id))
    assert b'User Group 1' not in response.data

def test_modify_study_user_group(client, init_database3):
        study = Study.query.filter_by(id=1).first()
        old_user_group = UserGroup.query.filter_by(id=1).first()
        new_user_group = UserGroup(name="User Group 1", study=study)
        db.session.add(new_user_group)
        db.session.commit()
        
        study = Study.query.filter_by(id=1).first()
        new_user_group = UserGroup.query.filter_by(id=2).first()
        old_user_group = UserGroup.query.filter_by(id=1).first()

        assert study.user_group_id == new_user_group.id
        assert old_user_group.study != study.user_group
