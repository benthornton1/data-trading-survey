from datetime import date
from urllib.parse import urlparse

from flask import url_for
from tests.helpers import create_study, login, create_participant, create_admin        

def test_login_required(client, init_database):
    """
    GIVEN a Flask application
    WHEN all routes with @login_required decorator are requested (GET)
    THEN check response location
    """
    with client.application.test_request_context():
        study = create_study(client)
    
        response = client.get(url_for('study.index'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('study.study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('study.user_info'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('study.change_info'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('study.complete'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        
        response = client.get(url_for('responses.general', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.heat_maps', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.compare_responses', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.average_response', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.create_pdf', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        
        response = client.get(url_for('admin.index'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.new_study'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.new_card_set'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.new_user_group'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        
        
def test_admin_required(client, init_database):
    """
    GIVEN a Flask application, participant
    WHEN all routes with @admin_required decorator are requested (GET)
    THEN check response location
    """
    with client.application.test_request_context():
        create_participant(client, username='p', password='p')
        login(client, username='p', password='p')
        
        study = create_study(client)
        
        response = client.get(url_for('responses.general', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.heat_maps', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.compare_responses', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.average_response', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.create_pdf', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        
        response = client.get(url_for('admin.index'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.new_study'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.new_card_set'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.new_user_group'), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        
        client.get(url_for('auth.logout'))
        
def test_valid_admin_required(client, init_database):
    """
    GIVEN a Flask application, admin
    WHEN all routes with @valid_admin_required decorator are requested (GET)
    THEN check response location
    """
    
    with client.application.test_request_context():
        admin = create_admin(client, username='a', password='a')
        login(client, username='a', password='a')
        
        study = create_study(client)
        
        response = client.get(url_for('responses.general', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.heat_maps', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.compare_responses', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.average_response', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('responses.create_pdf', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        
        response = client.get(url_for('admin.study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        response = client.get(url_for('admin.delete_study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('auth.login')
        
def test_check_delete(client, init_database):
    """
    GIVEN a Flask application, admin
    WHEN all routes with @check_delete decorator are requested (GET)
    THEN check response location
    """
    
    with client.application.test_request_context():
        admin = create_admin(client, username='a', password='a')
        login(client, username='a', password='a')
        
        study = create_study(client, creator=admin)
        
        response = client.get(url_for('admin.delete_user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('admin.index')
        response = client.get(url_for('admin.delete_card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('admin.index')
        response = client.get(url_for('admin.delete_study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('admin.index')
        
def test_check_edit(client, init_database):
    """
    GIVEN a Flask application, admin
    WHEN all routes with @check_edit decorator are requested (GET)
    THEN check response location
    """
    
    with client.application.test_request_context():
        admin = create_admin(client, username='a', password='a')
        login(client, username='a', password='a')
        
        study = create_study(client, creator=admin, start_date=date.today())
        
        response = client.get(url_for('admin.user_group', id=study.user_group.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('admin.index')
        response = client.get(url_for('admin.card_set', id=study.card_set_x.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('admin.index')
        response = client.get(url_for('admin.study', id=study.id), follow_redirects=False)
        assert urlparse(response.location).path == url_for('admin.index')
        