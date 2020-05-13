from app.responses.parsing.position_count import (
    get_card_x_responses,
    get_card_y_responses,
)
from tests.helpers import (
    create_admin,
    create_participant,
    create_response,
    create_study,
    create_user_group,
)


def test_get_card_x_responses(client, init_database):
    """
    GIVEN a Flask application, study, response
    WHEN get_card_x_responses is called 
    THEN check no error and return type
    """
    admin = create_admin(client)
    participant = create_participant(client)
    user_group = create_user_group(
        client, participants=[participant], creator=admin
    )
    study = create_study(client, creator=admin, user_group=user_group)
    response = create_response(
        client, study=study, creator=admin, participant=participant
    )

    updated_heat_maps = get_card_x_responses(study)

    assert isinstance(updated_heat_maps, tuple)


def test_get_card_y_responses(client, init_database):
    """
    GIVEN a Flask application, study, response
    WHEN get_card_y_responses is called
    THEN check no error and return type
    """
    admin = create_admin(client)
    participant = create_participant(client)
    user_group = create_user_group(
        client, participants=[participant], creator=admin
    )
    study = create_study(client, creator=admin, user_group=user_group)
    response = create_response(
        client, study=study, creator=admin, participant=participant
    )

    updated_heat_maps = get_card_y_responses(study)

    assert isinstance(updated_heat_maps, tuple)
