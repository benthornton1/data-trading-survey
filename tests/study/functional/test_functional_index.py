
from flask import url_for

from tests.helpers import login, create_admin, create_participant, create_study, create_user_group

def test_get_index(client, init_database):
    """
    GIVEN a Flask application, participant
    WHEN '/study' is requested (GET)
    THEN check status code and response content.
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        participant = create_participant(client, username='participant', password='password',gender='Male', age_group='20-29', country_of_birth='AF', latest_country='AX',
                       education_level='L6', occupation='Almoner', completed_form=True)

        login(client, username='participant', password='password')

        user_group = create_user_group(client, creator=admin, participants=[participant])
        study = create_study(client, creator=admin, user_group=user_group)
        
        response = client.get(url_for('study.index'), follow_redirects=True)
        
        assert response.status_code == 200
        assert bytes(study.name,'utf-8') in response.data
        assert bytes(study.description,'utf-8') in response.data
        if study.image:
            assert bytes(study.image,'utf-8') in response.data
        else:
            assert b'study_images/no_image.jpg' in response.data
        

def test_get_index_multiple_studies(client, init_database):
    """
    GIVEN a Flask application, participants, studies
    WHEN '/study' is requested (GET)
    THEN check status code and response content.
    """
    with client.application.test_request_context():
        admin = create_admin(client)
        participant = create_participant(client, username='participant', password='password',gender='Male', age_group='20-29', country_of_birth='AF', latest_country='AX',
                       education_level='L6', occupation='Almoner', completed_form=True)
        participant_2 = create_participant(client, username='participant_2', password='password',gender='Male', age_group='20-29', country_of_birth='AF', latest_country='AX',
                       education_level='L6', occupation='Almoner', completed_form=True)

        login(client, username='participant', password='password')

        user_group = create_user_group(client, creator=admin, participants=[participant])
        study = create_study(client, creator=admin, user_group=user_group)
        
        user_group_2 = create_user_group(client, creator=admin, participants=[participant_2])
        study_2 = create_study(client, name='Test Study 2', description='Test Study Description', creator=admin, user_group=user_group_2)
        
        response = client.get(url_for('study.index'), follow_redirects=True)
        
        assert response.status_code == 200
        assert bytes(study.name,'utf-8') in response.data
        assert bytes(study.description,'utf-8') in response.data
        if study.image:
            assert bytes(study.image,'utf-8') in response.data
        else:
            assert b'study_images/no_image.jpg' in response.data
        
        
        assert bytes(study_2.name,'utf-8') not in response.data
        assert bytes(study_2.description,'utf-8') not in response.data
        
        
        client.get(url_for('auth.logout'))
        login(client, username='participant_2', password='password')
        
        
        response = client.get(url_for('study.index'), follow_redirects=True)

        assert response.status_code == 200
        assert bytes(study_2.name,'utf-8') in response.data
        assert bytes(study_2.description,'utf-8') in response.data
        if study_2.image:
            assert bytes(study_2.image,'utf-8') in response.data
        else:
            assert b'study_images/no_image.jpg' in response.data