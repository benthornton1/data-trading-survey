from urllib.parse import urlparse

from flask import url_for

from tests.helpers import create_admin, create_participant, login, create_response, create_study, create_user_group

def test_get_average_response(client, init_database):
    """
    GIVEN a Flask application, admin, study, responses
    WHEN '/responses/average_response/<int:id>' is requested (GET)
    THEN check response content, status code
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        
        participant_1 = create_participant(client, username='p1')
        participant_2 = create_participant(client, username='p2')
        
        user_group = create_user_group(client, creator=admin, participants=[participant_1, participant_2])
        
        study = create_study(client, creator=admin, user_group=user_group)
        study_response_1 = create_response(client, participant=participant_1, creator=admin, study=study)
        study_response_2 = create_response(client, participant=participant_2, creator=admin, study=study)
        
        login(client, username='admin', password='password')

        response = client.get(url_for('responses.average_response', id=study.id), follow_redirects=True)
        
        assert response.status_code == 200
        for card in study.card_set_x.cards:
            assert bytes(card.name, 'utf-8') in response.data
            assert bytes(card.description, 'utf-8') in response.data
            assert bytes(card.image, 'utf-8') in response.data
        
        assert bytes('Highest '+study.card_set_x.measure, 'utf-8') in response.data
        assert bytes('Lowest '+study.card_set_x.measure, 'utf-8') in response.data

        for card in study.card_set_y.cards:
            assert bytes(card.name, 'utf-8') in response.data
            assert bytes(card.description, 'utf-8') in response.data
            assert bytes(card.image, 'utf-8') in response.data
        
        assert bytes('Highest '+study.card_set_y.measure, 'utf-8') in response.data
        assert bytes('Lowest '+study.card_set_y.measure, 'utf-8') in response.data

        assert bytes(study.data_value_labels[0].label, 'utf-8') in response.data
        
        client.get(url_for('auth.logout'))
        admin2 = create_admin(client, username='admin2', password='password')
        login(client, username='admin2', password='password')
        
        response = client.get(url_for('responses.average_response', id=study.id), follow_redirects=False)
        
        assert urlparse(response.location).path == url_for('auth.login')
    