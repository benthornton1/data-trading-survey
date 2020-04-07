
from flask import url_for

from app.study.forms import UserInfoForm
from tests.helpers import create_participant

def test_valid_login(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/auth/login' is posted with VALID credentials (POST)
    THEN check response is valid and user is logged in
    """
    with client.application.test_request_context():

        participant = create_participant(client, username='participant', password='IoTData')
        response = client.post(url_for('auth.login'),
                                    data=dict(username='participant', password='IoTData'),
                                    follow_redirects=True)
        
        form = UserInfoForm()
        assert response.status_code == 200
        assert bytes(form.gender.label.text, 'utf-8') in response.data
        for choice in form.gender.iter_choices():
            assert bytes(choice[1], 'utf-8') in response.data
        assert bytes(form.age_group.label.text, 'utf-8') in response.data
        for choice in form.age_group.iter_choices():
            assert bytes(choice[1], 'utf-8') in response.data
        assert bytes(form.nationality.label.text, 'utf-8') in response.data
        for choice in form.nationality.iter_choices():
            assert bytes(choice[1], 'utf-8') in response.data
        assert bytes(form.latest_country.label.text, 'utf-8') in response.data
        for choice in form.latest_country.iter_choices():
            assert bytes(choice[1], 'utf-8') in response.data
        assert bytes(form.education_level.label.text, 'utf-8') in response.data
        for choice in form.education_level.iter_choices():
            assert bytes(choice[1], 'utf-8') in response.data
        assert bytes(form.occupation.label.text, 'utf-8') in response.data
        for choice in form.occupation.iter_choices():
            assert bytes(choice[1], 'utf-8') in response.data
        assert bytes(form.income.label.text, 'utf-8') in response.data
        for choice in form.income.iter_choices():
            assert bytes(choice[1], 'utf-8') in response.data
        assert bytes(form.submit.label.text, 'utf-8') in response.data
    

        client.get('auth.logout')

def test_logout_logged_in(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/auth/logout' is requested when logged in (GET)
    THEN check response is valid and user is logged out
    """
    # login
    with client.application.test_request_context():
        participant = create_participant(client, username='participant', password='IoTData')
        response = client.post(url_for('auth.login'),
                                    data=dict(username='participant', password='IoTData'),
                                    follow_redirects=True)
        assert response.status_code == 200    
        # logout
        response = client.get(url_for('auth.logout'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Sign In" in response.data
        assert b"Username" in response.data
        assert b"Password" in response.data
    
def test_logout_not_logged_in(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/auth/logout' is requested when not logged in (GET)
    THEN check response is valid and user is logged out
    """
    with client.application.test_request_context():
        response = client.get(url_for('auth.logout'), follow_redirects=True)
        assert response.status_code == 200
        assert b"Sign In" in response.data
        assert b"Username" in response.data