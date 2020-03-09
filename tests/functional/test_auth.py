

def test_true_admin_login(client, init_database):
    response = client.post('/auth/login',
                                data=dict(username='ben@hotmail.com', password='IoTData'),
                                follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'http://localhost/admin'

    response = client.get(response.location)
    assert response.status_code == 200
    assert b'Hello, ben' in response.data
    client.get('/auth/logout')

def test_incorrect_admin_login(client, init_database):
    response = client.post('/auth/login',
                                data=dict(username='ben@hotmail.com', password='hey'),
                                follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'http://localhost/auth/login'
    
def test_participant_login(client, init_database):
    response = client.post('/auth/login',
                                data=dict(username='harry@gmail.com', password='flask'),
                                follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'http://localhost/study/user_info'
    
    response = client.get(response.location)
    assert response.status_code == 200
    client.get('/auth/logout')
    
def test_incorrect_participant_login(client, init_database):
    response = client.post('/auth/login',
                                data=dict(username='harry@gmail.com', password='password'),
                                follow_redirects=False)
    assert response.status_code == 302
    assert response.location == 'http://localhost/auth/login'

    