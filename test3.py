from app import db, create_app
from app.models import Card, CardSet, DataValuesLabels, Response, Study, User, UserGroup
from datetime import date, timedelta


app = create_app()
    
with app.app_context():
    try:
        responses = Response.query.all()
        for response in responses:
            db.session.delete(response)
        
        db.session.commit()
        responses = Response.query.all()
        
        # {'cards_x': {'0': ['1'], '1': [], '2': [], '3': []}, 'cards_y': {'0': [], '1': [], '2': [], '3': ['2']}, 'data_values': {'col-0-row-3': ['12'], 'col-1-row-3': [''], 'col-2-row-3': [''], 'col-3-row-3': [''], 'col-0-row-2': [''], 'col-1-row-2': [''], 'col-2-row-2': [''], 'col-3-row-2': [''], 'col-0-row-1': [''], 'col-1-row-1': [''], 'col-2-row-1': [''], 'col-3-row-1': [''], 'col-0-row-0': [''], 'col-1-row-0': [''], 'col-2-row-0': [''], 'col-3-row-0': ['']}}
        cards_x={'0': [], '1': [], '2': ['1'], '3': []}
        cards_y={'0': [], '1': ['2'], '2': [], '3': []}
        data_values = {'col-0-row-3': ['6'], 'col-1-row-3': [''], 'col-2-row-3': [''], 'col-3-row-3': [''], 'col-0-row-2': [''], 'col-1-row-2': [''], 'col-2-row-2': [''], 'col-3-row-2': [''], 'col-0-row-1': [''], 'col-1-row-1': [''], 'col-2-row-1': [''], 'col-3-row-1': [''], 'col-0-row-0': [''], 'col-1-row-0': [''], 'col-2-row-0': [''], 'col-3-row-0': ['']}
        r1 = Response(study=1,cards_x=cards_x, cards_y=cards_y, data_values=data_values)
        cards_x={'0': ['1'], '1': [], '2': [], '3': []}
        cards_y={'0': ['2'], '1': [], '2': [], '3': []}
        data_values = {'col-0-row-3': ['52'], 'col-1-row-3': [''], 'col-2-row-3': [''], 'col-3-row-3': [''], 'col-0-row-2': [''], 'col-1-row-2': [''], 'col-2-row-2': [''], 'col-3-row-2': [''], 'col-0-row-1': [''], 'col-1-row-1': [''], 'col-2-row-1': [''], 'col-3-row-1': [''], 'col-0-row-0': [''], 'col-1-row-0': [''], 'col-2-row-0': [''], 'col-3-row-0': ['']}
        r2 = Response(study=1,cards_x=cards_x, cards_y=cards_y, data_values=data_values)
        cards_x={'0': ['1'], '1': [], '2': [], '3': []}
        cards_y={'0': [], '1': [], '2': [], '3': ['2']}
        data_values = {'col-0-row-3': ['52'], 'col-1-row-3': [''], 'col-2-row-3': [''], 'col-3-row-3': [''], 'col-0-row-2': [''], 'col-1-row-2': [''], 'col-2-row-2': [''], 'col-3-row-2': [''], 'col-0-row-1': [''], 'col-1-row-1': [''], 'col-2-row-1': [''], 'col-3-row-1': [''], 'col-0-row-0': [''], 'col-1-row-0': [''], 'col-2-row-0': [''], 'col-3-row-0': ['']}
        r3 = Response(study=1,cards_x=cards_x, cards_y=cards_y, data_values=data_values)
        
        
        db.session.add(r1)
        db.session.add(r2)
        db.session.add(r3)
        db.session.commit()
    
    except Exception as error:
        print(str(error))
        db.session.rollback()