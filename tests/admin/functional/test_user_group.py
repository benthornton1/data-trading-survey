
from datetime import date, timedelta
from urllib.parse import urlparse

from flask.helpers import url_for
from flask_login import current_user,login_user

from app.admin.forms import UserGroupForm
from app.models import Participant, UserGroup
from tests.helpers import create_admin, create_participant, create_study, create_user_group, login

def test_create_valid_user_group(client, init_database):
    """
    GIVEN a Flask application, logged in admin
    WHEN '/admin/new_user_group/1' is requested (GET)
    WHEN '/admin/study/1' is posted with valid data (POST).
    THEN check response is valid and the user group has been created.
    """
    
    user_group_form = UserGroupForm()
    
    data = {'name': 'Test', 'users': [{'email': 'test@test.com'}, {'email': 'b@b.com'}], 'submit': True}
    user_group_form.name.data = "User Group 1"
    user_group_form.users.pop_entry()
    user_group_form.users.append_entry({'email':'test@test.com'})
    user_group_form.submit.data = True

    with client.application.test_request_context():

        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        client.get(url_for('admin.new_user_group'))
        response = client.post(url_for('admin.user_group', id=1), data=user_group_form.data, follow_redirects=True)

        assert response.status_code == 200
        assert b"User Group 1" in response.data
        
        user_group = UserGroup.query.filter_by(id=1).first()
        
        assert user_group.name == "User Group 1"
        assert user_group.users[0].email == "test@test.com"
        
    
def test_create_invalid_user_group(client, init_database):
    """
    GIVEN a Flask application, logged in admin
    WHEN '/admin/new_user_group' is requested (GET)
    WHEN '/admin/study/1' is posted with invalid data (POST).
    THEN check response is valid and the user group has not been created.
    """
    user_group_form = UserGroupForm()
    
    user_group_form.name.data = "User Group 1"
    user_group_form.users.pop_entry()
    user_group_form.users.append_entry('test.com')
    user_group_form.submit.data = True
    with client.application.test_request_context():

        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        client.get(url_for('admin.new_user_group'))
        response = client.post(url_for('admin.user_group', id=1), data=user_group_form.data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"[email]" in response.data
    
def test_delete_current_user_group(client, init_database):
    """
    GIVEN a Flask application, logged in admin, and a user group added to a current study
    WHEN '/admin/delete_study/1' is requested (GET)
    THEN check response is valid and the user group has not been deleted.
    """
    with client.application.test_request_context():
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        
        user_group = create_user_group(client, creator=admin)
        study = create_study(client, name="Test Study", creator=admin, user_group=user_group)
        
        response = client.get(url_for('admin.delete_user_group', id=user_group.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert b'You cannot delete this User Group as it is currently associated with Test Study Study, remove this association before deleting this User Group.' in response.data

        user_group_db = UserGroup.query.filter_by(id=user_group.id).first()
        
        assert user_group_db.name == user_group.name
        assert user_group_db.creator == user_group.creator
        assert user_group_db.users == user_group.users
        assert user_group_db.study == user_group.study
    
def test_delete_future_user_group(client, init_database):
    """
    GIVEN a Flask application, logged in admin, and a user group added to a future study
    WHEN '/admin/delete_study/1' is requested (GET)
    THEN check response is valid and the user group has not been deleted.
    """
    with client.application.test_request_context():

        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        
        user_group = create_user_group(client, creator=admin)
        study = create_study(client, creator=admin, user_group=user_group, start_date=date.today()+timedelta(days=1))
        
        response = client.get(url_for('admin.delete_user_group', id=user_group.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert b'You cannot delete this User Group as it is currently associated with Test Study Study, remove this association before deleting this User Group.' in response.data

        user_group_db = UserGroup.query.filter_by(id=user_group.id).first()
        
        assert user_group_db is not None
        assert user_group_db.name == user_group.name
        assert user_group_db.creator == admin
        assert user_group_db.study == study
        assert user_group_db.name == user_group.name
        
def test_delete_user_group(client, init_database):
    """
    GIVEN a Flask application, logged in admin, and a user group
    WHEN '/admin/delete_study/1' is requested (GET)
    THEN check response is valid and the user group has been deleted.
    """
    with client.application.test_request_context():

        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        
        user_group = create_user_group(client, name="Test User Group", creator=admin)
        
        response = client.get(url_for('admin.delete_user_group', id=user_group.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert b'User Group Test User Group succesfully deleted.' in response.data
        
        user_group_db = UserGroup.query.filter_by(id=user_group.id).first()
        participants = Participant.query.all()
        
        assert user_group_db is None
        assert participants == []

    
def test_edit_current_user_group(client, init_database):
    """
    GIVEN a Flask application, logged in admin, and a user group added to a current study
    WHEN '/admin/study/1' is requested (GET)
    THEN check response is valid and the user group cannot be edited.
    """
    with client.application.test_request_context():
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        
        user_group = create_user_group(client, creator=admin)
        study = create_study(client, creator=admin, user_group=user_group, start_date=date.today())
        
        response = client.get(url_for('admin.user_group', id=user_group.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert b"You cannot edit this User Group as the Study associated with it is currently in progress." in response.data
    
def test_edit_future_user_group(client, init_database):
    """
    GIVEN a Flask application, logged in admin, and a user group added to a future study
    WHEN '/admin/study/1' is requested (GET)
    THEN check response is valid and the user group can be edited.
    """
    with client.application.test_request_context():
    
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        
        user_group = create_user_group(client, creator=admin)
        study = create_study(client, creator=admin, user_group=user_group, start_date=date.today()+timedelta(days=1))
        
        response = client.get(url_for('admin.user_group', id=user_group.id), follow_redirects=True)
        
        assert response.status_code == 200
        for user in study.user_group.users:
            assert bytes(user.email, 'utf-8') in response.data
                
        form = UserGroupForm()
        assert bytes(form.name.label.text, 'utf-8') in response.data
        assert bytes(form.users.label.text, 'utf-8') in response.data
        
        user_group_form = UserGroupForm()
    
        user_group_form.name.data = "Edited User Group 1"
        user_group_form.users.pop_entry()
        user_group_form.users.append_entry('test2@test.com')
        user_group_form.submit.data = True
        
        response = client.post(url_for('admin.user_group', id=1), data=user_group_form.data, follow_redirects=True)
        
        assert response.status_code == 200
        
        user_group = UserGroup.query.filter_by(id=1).first()
        
        assert user_group.name == "Edited User Group 1"
        assert user_group.users[0].email == "test2@test.com"
        
        