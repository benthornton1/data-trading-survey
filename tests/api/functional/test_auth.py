
from flask.helpers import url_for
from flask_jwt_extended import decode_token

from tests.helpers import create_admin

def test_valid_login(client, init_database):
    """
    GIVEN a Flask Application, logged in admin
    WHEN '/api/login' is posted with valid data (POST)
    THEN check response is valid and access token is valid
    """
    with client.application.test_request_context():
        admin = create_admin(client, username='admin', password='IoTData')
        "Content-Type: application/json"
        response = client.post(url_for('api.login'), 
                            json=dict(username='admin', password='IoTData'))
        
        assert response.status_code == 200
        assert 'access_token' in response.json
        assert 'jti' in decode_token(response.json['access_token'])

    
