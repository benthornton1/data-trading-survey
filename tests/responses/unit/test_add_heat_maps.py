from app.responses.parsing.add_heat_maps import (
    CreateOneHeatMapCount,
    CreateOneHeatMap,
)

from tests.helpers import (
    create_admin,
    create_data_value_label,
    create_participant,
    create_response,
    create_study,
    create_user_group,
)

from app.models import DataValue, CardPosition, Card
from app import db


def test_CreateOneHeatMap(client, init_database):
    """
    GIVEN a Flask application, study, response
    WHEN CreateOneHeatMap.add is called 
    THEN check no error and content
    """
    admin = create_admin(client)
    participant = create_participant(client)
    user_group = create_user_group(
        client, participants=[participant], creator=admin
    )
    study = create_study(
        client, creator=admin, user_group=user_group, data_value_labels=[]
    )
    response = create_response(
        client, study=study, creator=admin, participant=participant
    )

    c = CreateOneHeatMap(study)
    c.add(
        study.card_set_x.cards[0], study.card_set_y.cards[0], study.data_value_labels[0]
    )
    plot = c.plots

    assert isinstance(plot, list)
    assert isinstance(plot[0], tuple)
    assert len(plot) == 1


def test_CreateOneHeatMapCount(client, init_database):
    """
    GIVEN a Flask application, study, response
    WHEN CreateOneHeatMapCount.add is called 
    THEN check no error and content
    """
    admin = create_admin(client)
    participant = create_participant(client)
    user_group = create_user_group(
        client, participants=[participant], creator=admin
    )
    study = create_study(
        client, creator=admin, user_group=user_group, data_value_labels=[]
    )
    response = create_response(
        client, study=study, creator=admin, participant=participant
    )

    c = CreateOneHeatMapCount(study)
    c.add(
        study.card_set_x.cards[0], study.card_set_y.cards[0], None
    )
    plot = c.plots

    assert isinstance(plot, list)
    assert isinstance(plot[0], tuple)
    assert len(plot) == 1

def test_calculate_price(client, init_database):
    """
    GIVEN a Flask application, study, responses
    WHEN CreateHeatMap.calculate_price is called 
    THEN check returned data
    """
    admin = create_admin(client)
    participant_1 = create_participant(client)
    participant_2 = create_participant(client, username='p2')
    user_group = create_user_group(
        client, participants=[participant_1, participant_2], creator=admin
    )
    study = create_study(
        client, creator=admin, user_group=user_group, data_value_labels=[]
    )
    response_1 = create_response(
        client, study=study, creator=admin, participant=participant_1
    )
    response_2 = create_response(
        client, study=study, creator=admin, participant=participant_2
    )
    
    dv1 = DataValue.query.filter(DataValue.response==response_1).filter(DataValue.column==0).filter(DataValue.row==1).filter(DataValue.data_value_label==study.data_value_labels[0]).first()
    dv2 = DataValue.query.filter(DataValue.response==response_2).filter(DataValue.column==0).filter(DataValue.row==1).filter(DataValue.data_value_label==study.data_value_labels[0]).first()
    val_1 = 100
    val_2 = 50
    dv1.value = val_1
    dv2.value = val_2
    
    c_1 = Card.query.filter_by(name='Entertainment').first()
    c_2 = Card.query.filter_by(name='Health Service').first()
    for pos in c_1.positions:
        pos.position=0
    for pos in c_2.positions:
        pos.position=1
    
    
    db.session.commit()
    max_val = float('-inf')
    min_val = float('inf')
    for data_value in response_1.data_values:
        if data_value.data_value_label == study.data_value_labels[0]:
            if data_value.value > max_val:
                max_val = data_value.value
            if data_value.value < min_val:
                min_val = data_value.value
    
    normalised_1 = (val_1-min_val)/(max_val-min_val)
    
    max_val = float('-inf')
    min_val = float('inf')
    
    for data_value in response_2.data_values:
        if data_value.data_value_label == study.data_value_labels[0]:
            if data_value.value > max_val:
                max_val = data_value.value
            if data_value.value < min_val:
                min_val = data_value.value
    
    normalised_2 = (val_2-min_val)/(max_val-min_val)
    
    avg_normalised = (normalised_1 + normalised_2)/2
    
    c = CreateOneHeatMapCount(study)
    
    data = c.calculate_price(card_x=c_1, card_y=c_2, data_value_label=study.data_value_labels[0])
    assert avg_normalised in data["values"]


def test_calculate_count(client, init_database):
    """
    GIVEN a Flask application, study, responses
    WHEN CreateHeatMap.calculate_count is called 
    THEN check returned data
    """
    
    admin = create_admin(client)
    participant_1 = create_participant(client)
    participant_2 = create_participant(client, username='p2')
    user_group = create_user_group(
        client, participants=[participant_1, participant_2], creator=admin
    )
    study = create_study(
        client, creator=admin, user_group=user_group, data_value_labels=[]
    )
    response_1 = create_response(
        client, study=study, creator=admin, participant=participant_1
    )
    response_2 = create_response(
        client, study=study, creator=admin, participant=participant_2
    )
    
    c_1 = Card.query.filter_by(name='Entertainment').first()
    c_2 = Card.query.filter_by(name='Health Service').first()
    
    c = CreateOneHeatMapCount(study)
    data = c.calculate_count(c_1,c_2)
    
    assert 2 in data["values"]
    