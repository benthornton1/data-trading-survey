from urllib.parse import urlparse
from datetime import date, timedelta

from flask import get_flashed_messages, flash, url_for

from app import db
from app.admin.forms import CardForm, CardSetForm
from app.models import Card, CardSet, Study
from tests.helpers import create_admin, create_card_set, create_study, login


def test_create_valid_card_set(client, init_database):
    """
    GIVEN a Flask application
    WHEN '/admin/create_study/1' is requested (GET)
    WHEN '/admin/card_set/1' is posted with VALID data (POST)
    THEN check response is valid and card set is created with the data.
    """
    with client.application.test_request_context():

        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        
        card_data = dict(card_name = "Card 1", measure="Measure 1")
        card_set_data = dict(card_set_name = "Card Set 1", cards = card_data,measure = "Sensitivity")
        
        response = client.get(url_for('admin.new_card_set'))
        
        assert urlparse(response.location).path == url_for('admin.card_set', id=1)
        
        response = client.get(response.location, follow_redirects=True)
        
        form = CardSetForm()
        assert response.status_code == 200
        assert bytes(form.card_set_name.label.text, 'utf-8') in response.data
        assert bytes(form.measure.label.text, 'utf-8') in response.data
        
        response = client.post(url_for('admin.card_set', id=1), data=card_set_data, follow_redirects=True)
        
        assert response.status_code == 200
        assert b"Card Set 1" in response.data
    
def test_create_invalid_card_set(client, init_database):
    """
    GIVEN a Flask application, logged in admin
    WHEN '/admin/create_study/1' is requested (GET)
    WHEN '/admin/card_set/1' is posted with INVALID data (POST)
    THEN check response is valid and card set is not created with the data.
    """
    with client.application.test_request_context():

        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        
        card_data = dict(card_name = "Card 1")
        card_set_data = dict(card_set_name = "Card Set 1", cards = card_data,measure = "Sensitivity")
        
        response = client.get(url_for('admin.new_card_set'))
        
        assert urlparse(response.location).path == url_for('admin.card_set', id=1)
        
        response = client.post(url_for('admin.card_set', id=1), data=card_set_data)

        assert response.status_code == 200
        assert b"[This field is required.]" in response.data
        
        response = client.get(url_for('admin.index'))
                
        assert b"Card Set 1" not in response.data

        
def test_delete_current_card_set(client, init_database):
    """
    GIVEN a Flask application, logged in admin and card set which is added to a current study
    WHEN '/admin/delete_card_set/1' is requested (GET)
    THEN check response is valid and card set is not deleted.
    """
    
    with client.application.test_request_context():
 
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        card_set = create_card_set(client, name="Test Card Set", creator=admin)
        study = create_study(client, card_set_x=card_set, creator=admin, start_date=date.today())

        response = client.get(url_for('admin.delete_card_set', id=card_set.id), follow_redirects=True)

        assert response.status_code == 200
        assert b'You cannot delete this Card Set as it is currently associated with &#39;Test Study&#39; Studies, remove these associations before deleting this Card Set.' in response.data
        
        card_set_db = CardSet.query.filter_by(id=1).first()
        
        assert card_set_db.name == card_set.name
        assert card_set_db.measure == card_set.measure
        assert card_set_db.cards == card_set.cards
        
        study.card_set_x = None
        db.session.commit()
        
        response = client.get(url_for('admin.delete_card_set', id=card_set.id), follow_redirects=True)
        
        card_set_db = CardSet.query.filter_by(id=1).first()
        
        assert response.status_code == 200
        assert card_set_db is None
        assert b'Card Set Test Card Set succesfully deleted' in response.data
    
def test_delete_future_card_set(client, init_database):
    """
    GIVEN a Flask application, logged in admin and card set which is added to a future study
    WHEN '/admin/delete_card_set/1' is requested (GET)
    THEN check response is valid and card set is deleted.
    """
    with client.application.test_request_context():
 
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        card_set = create_card_set(client, name="Test Card Set", creator=admin)
        study = create_study(client, card_set_x=card_set, creator=admin, start_date=date.today()+timedelta(days=3))
        
        response = client.get(url_for('admin.delete_card_set', id=card_set.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert b'You cannot delete this Card Set as it is currently associated with &#39;Test Study&#39; Studies, remove these associations before deleting this Card Set.' in response.data
        
        card_set_db = CardSet.query.filter_by(id=1).first()
        
        assert card_set_db.name == card_set.name
        assert card_set_db.measure == card_set.measure
        assert card_set_db.cards == card_set.cards
        
        study.card_set_x = None
        db.session.commit()
        
        response = client.get(url_for('admin.delete_card_set', id=card_set.id), follow_redirects=True)
        
        card_set_db = CardSet.query.filter_by(id=1).first()
        
        assert response.status_code == 200
        assert card_set_db is None
        assert b'Card Set Test Card Set succesfully deleted' in response.data

def test_delete_card_set(client, init_database):
    """
    GIVEN a Flask application, logged in admin and card set which is added to a future study
    WHEN '/admin/delete_card_set/1' is requested (GET)
    THEN check response is valid and card set is deleted.
    """
    with client.application.test_request_context():
 
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        card_set = create_card_set(client, name="Test Card Set", creator=admin)
        
        response = client.get(url_for('admin.delete_card_set', id=card_set.id), follow_redirects=True)
        
        card_set_db = CardSet.query.filter_by(id=1).first()
        cards = Card.query.all()
        
        assert response.status_code == 200
        assert card_set_db is None
        assert cards == []
        assert b'Card Set Test Card Set succesfully deleted' in response.data
        
def test_edit_current_card_set(client, init_database):
    """
    GIVEN a Flask application, logged in admin, and card set which is added to a current study
    WHEN '/admin/card_set/1' is requested (GET)
    THEN check response is valid and card set cannot be edited.
    """
    with client.application.test_request_context():
 
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        card_set = create_card_set(client, creator=admin)
        study = create_study(client, creator=admin, card_set_y=card_set)
        
        response = client.get(url_for('admin.card_set', id=card_set.id), follow_redirects=True)
        
        assert response.status_code == 200
        assert b'You cannot edit this Card Set as there are Studies associated with it which are currently in progress.' in response.data
        
        card_set_db = CardSet.query.first()
        
        assert card_set_db.name == card_set.name
        assert card_set_db.measure == card_set.measure
        assert card_set_db.cards == card_set.cards
        assert card_set_db.creator == admin
        
        client.get(url_for('auth.logout'))

def test_edit_future_card_set(client, init_database):
    """
    GIVEN a Flask application, logged in admin and card set which is added to a future study
    WHEN '/admin/card_set/1' is requested (GET)
    THEN check response is valid and card set can be edited.
    """
    with client.application.test_request_context():
 
        admin = create_admin(client, username='admin', password='password')
        login(client, username='admin', password='password')
        card_set = create_card_set(client, creator=admin)
        study = create_study(client, creator=admin, card_set_x=card_set, start_date=date.today()+timedelta(days=3))

        response = client.get(url_for('admin.card_set', id=study.card_set_x.id), follow_redirects=True)
        
        assert response.status_code == 200
        for card in card_set.cards:
            assert bytes(card.name, 'utf-8') in response.data
            assert bytes(card.description, 'utf-8') in response.data
        
        form_card = CardForm(card_name= "Updated Card", image=None, desc="Updated Description")
        form_card_set = CardSetForm()
        form_card_set.card_set_name.data = "Updated Card Set"
        form_card_set.cards.pop_entry()
        form_card_set.cards.append_entry({'card_name' : "Updated Card", 'image':None, 'desc':"Updated Description"})
        # form_card_set.cards.append_entry(form_card)
        form_card_set.measure.data = "Updated Measure"

        response = client.post(url_for('admin.card_set', id=study.card_set_x.id), data=form_card_set.data, follow_redirects=True)

        assert study.card_set_x.name == "Updated Card Set"
        assert study.card_set_x.measure == "Updated Measure"
        assert study.card_set_x.cards[0].name == "Updated Card"
        assert study.card_set_x.cards[0].image == "updatedimage.jpg"
        assert study.card_set_x.cards[0].description == "Updated Description"
        assert len(study.heat_maps) == (len(study.card_set_x.cards)*len(study.card_set_y.cards)*len(study.data_value_labels)*2)
