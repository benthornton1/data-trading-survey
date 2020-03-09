from app.models import User, UserGroup
from app import db
from flask.helpers import url_for

def participant_login(client, username, password):
    return client.post('/auth/login',
                            data=dict(username=username, password=password),
                            follow_redirects=False)
    

def test_user_info_load(client, init_database3):
    response = participant_login(client=client, username='harry@gmail.com', password='flask')
    assert response.location == 'http://localhost/study/user_info'
    
def test_study_loads(client, init_database3):
    with client:
        user = User.query.filter_by(id=2).first()
        user.completed_form = True
        db.session.commit()
        
        participant_login(client=client, username='harry@gmail.com', password='flask')

        response = client.get('http://localhost/study/1', follow_redirects=False)
        
        assert response.status_code == 200
        assert response.location != 'http://localhost/study/'
        
def test_study_redirects_with_incorrect_user(client, init_database3):
    
    new_user = User(id=3, username="test", completed_form=True)
    new_user.set_password("test")
    new_user_group = UserGroup(id=2, name="User Group 2", users=[new_user])
    
    db.session.add(new_user)
    db.session.add(new_user_group)
    db.session.commit()
    participant_login(client=client, username="test", password="test")
    
    response = client.get('http://localhost/study/1', follow_redirects=False)
    
    assert response.status_code == 302
    assert response.location == 'http://localhost/study/'
    
    
    
    