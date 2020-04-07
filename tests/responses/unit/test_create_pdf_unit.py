import os

from app.responses.parsing.create_pdf import create_pdf
from tests.helpers import create_admin, create_participant, create_response, create_study, create_user_group, login


def test_create_pdf(client, init_database):
    """
    GIVEN a Flask application, study
    WHEN create_pdf is called 
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
        
        
        file_path_1 = create_pdf(study, all_responses=True)
        
        assert isinstance(file_path_1, str)
        path = 'app'+file_path_1
        assert os.path.exists(path) is True
        
        file_path_2 = create_pdf(study, average_response2=True)
        
        assert isinstance(file_path_2, str)
        path = 'app'+file_path_2
        assert os.path.exists(path) == True
        assert file_path_1 != file_path_2
        
        file_path_3 = create_pdf(study, response_ids=[response_1.id, response_3.id])
        
        assert isinstance(file_path_3, str)
        path = 'app'+file_path_3
        assert os.path.exists(path) == True
        assert file_path_2 != file_path_3
        assert file_path_1 != file_path_3
        
        file_path_4 = create_pdf(study, average_response2=True, response_ids=[response_1.id, response_3.id])
        
        assert isinstance(file_path_4, str)
        path = 'app'+file_path_4
        assert os.path.exists(path) == True
        assert file_path_3 != file_path_4
        assert file_path_2 != file_path_4
        assert file_path_1 != file_path_4
        
        file_path_5 = create_pdf(study, average_response2=True, all_responses=True)
        
        assert isinstance(file_path_1, str)
        path = 'app'+file_path_5
        assert os.path.exists(path) == True
        assert file_path_4 != file_path_5
        assert file_path_3 != file_path_5
        assert file_path_2 != file_path_5
        assert file_path_1 != file_path_5