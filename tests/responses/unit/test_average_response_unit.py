from munch import munchify

from app.responses.parsing.average_response2 import average_response
from tests.helpers import create_admin, login, create_participant, create_response, create_study, create_user_group


def test_average_response(client, init_database):
    """
    GIVEN a Flask application, study, responses
    WHEN average_response is called 
    THEN check no error and return type
    """
    with client.application.test_request_context():
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        p1 = create_participant(client, username='p1')
        p2 = create_participant(client, username='p2')
        p3 = create_participant(client, username='p3')
        p4 = create_participant(client, username='p4')
        user_group = create_user_group(client, creator=admin, participants=[p1,p2,p3,p4])
        study = create_study(client, user_group=user_group, creator=admin)
        response_1 = create_response(client, study = study, participant=p1, creator=admin)
        response_2 = create_response(client, study = study, participant=p2, creator=admin)
        response_3 = create_response(client, study = study, participant=p3, creator=admin)
        response_4 = create_response(client, study = study, participant=p4, creator=admin)
        
        avg_response = munchify(average_response(study))
        
        assert avg_response.cards_x == munchify(response_1.cards_x)
        assert avg_response.cards_y == munchify(response_1.cards_y)
        assert avg_response.data_values == munchify(response_1.data_values)