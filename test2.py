from app import db, create_app
from app.models import Card, CardSet, DataValuesLabels, Study, User, UserGroup
from datetime import date, timedelta


app = create_app()
    
with app.app_context():
    try:
        print('hello')
        
        admin = User(id=1, username="admin", email="ben@ben.com", is_admin=True)
        admin.set_password('password')
        participant = User(id=2, username="participant", email="ben14367@hotmail.com")
        participant.set_password('password')
        card1 = Card(name='Card Num 1', desc="Desc card number 1", image='hi.jpg')
        card2 = Card(name="Card Num 2", desc="Desc card number 2", image='yay.jpg')
        card_set1 = CardSet(name="Card Set 1", measure="Sensitivity", cards=[card1], creator=admin.id)
        card_set2 = CardSet(name="Card Set 2", measure="Cost", cards=[card2], creator=admin.id)
        user_group1 = UserGroup(id=1, name="User Group 1", users=[participant], creator_id=admin.id)
        data_value_label = DataValuesLabels(label="hey")
        study1 = Study(name="Study 1", card_sets=[card_set1, card_set2], data_values=1, data_values_labels=[data_value_label], number_of_columns=4, number_of_rows=4, user_group_id=user_group1.id, creator=admin.id, start_date=date.today(), end_date=date.today()+timedelta(days=3) )
        data_value_label.study_id = 1
        user_group1.studies = [study1]
        
        db.session.add(admin)
        db.session.add(participant)
        db.session.add(card1)
        db.session.add(card2)
        db.session.add(card_set1)
        db.session.add(card_set2)
        db.session.add(user_group1)
        db.session.add(study1)
        db.session.commit()

    except Exception as error:
        print(str(error))
        db.session.rollback()