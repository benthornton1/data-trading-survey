from urllib.parse import urlparse

from flask.helpers import url_for

from tests.helpers import create_admin, create_study, login, create_participant

def test_get_index(client, init_database):
    """
    GIVEN a Flask application, admin, study
    WHEN '/admin' is requested (GET)
    THEN check response content, status code
    """
    with client.application.test_request_context():
        admin = create_admin(client, username='admin', password='password')
        
        study = create_study(client, creator=admin)
        login(client, username='admin', password='password')
        
        response = client.get(url_for('admin.index'), follow_redirects=True)

        assert response.status_code == 200
        assert bytes(study.name, 'utf-8') in response.data
        assert bytes(study.card_set_x.name, 'utf-8') in response.data
        assert bytes(study.card_set_y.name, 'utf-8') in response.data
        assert bytes(study.user_group.name, 'utf-8') in response.data
        assert bytes(study.description, 'utf-8') in response.data
        assert bytes(study.image, 'utf-8') in response.data
        assert bytes(str(study.number_of_columns), 'utf-8') in response.data
        assert bytes(str(study.number_of_rows), 'utf-8') in response.data
        assert bytes(str(study.start_date), 'utf-8') in response.data
        assert bytes(str(study.end_date), 'utf-8') in response.data
        assert bytes(study.name, 'utf-8') in response.data
        client.get(url_for('auth.logout'))
        
def test_get_index_multiple_admins(client, init_database):
    """
    GIVEN a Flask application, 2 admins, study created by 1st admin
    WHEN 2nd admin is logged in and '/admin' is requested (GET)
    THEN check response content, status code
    """
    with client.application.test_request_context():

        admin = create_admin(client, username='admin', password='password')
        admin2 = create_admin(client, username='admin2', password='password')
        
        
        study = create_study(client, creator=admin)
        login(client, username='admin2', password='password')
        
        response = client.get(url_for('admin.index'), follow_redirects=True)

        assert bytes(study.name, 'utf-8')  not in response.data
        assert bytes(study.user_group.name, 'utf-8') not in response.data
        assert bytes(study.card_set_x.name, 'utf-8') not in response.data
        assert bytes(study.card_set_y.name, 'utf-8') not in response.data
        client.get(url_for('auth.logout'))
