from flask import url_for

from tests.helpers import create_participant, login

def test_participant_error_handler_404(client, init_database):
    """
    GIVEN a Flask application, logged in participant
    WHEN '/<path:unkown_path>' is requested (GET)
    THEN check response content, status code
    """
    
    with client.application.test_request_context():
        create_participant(client, username='participant', password='password')
        login(client, username='participant', password='password')
        
        response = client.get('/no_resource_found_here', follow_redirects=True)
        
        assert response.status_code == 404
        assert b'Error :(' in response.data
        assert b'404 Not Found' in response.data
        assert b'Go Back' in response.data
        assert bytes(url_for('study.index'), 'utf-8') in response.data
        client.get(url_for('auth.logout'))
        
def test_participant_error_handler_405(client, init_database):
    """
    GIVEN a Flask application, logged in participant
    WHEN '/study/user_info' is posted (POST)
    THEN check response content, status code
    """
    
    with client.application.test_request_context():
        create_participant(client, username='participant', password='password', completed_form=True)
        login(client, username='participant', password='password')
        
        response = client.post(url_for('study.index'), follow_redirects=True)
        
        assert response.status_code == 405
        assert b'Error :(' in response.data
        assert b'405 Method Not Allowed' in response.data
        assert b'Go Back' in response.data
        assert bytes(url_for('study.index'), 'utf-8') in response.data
        client.get(url_for('auth.logout'))