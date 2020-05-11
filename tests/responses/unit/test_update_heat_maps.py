from app.responses.parsing.update_heat_maps import update_heat_maps
from tests.helpers import (
    create_admin,
    create_participant,
    create_response,
    create_study,
    create_user_group,
)


def test_update_heat_map(client, init_database):
    """
    GIVEN a Flask application
    WHEN update_heat_maps is called with new response
    THEN check no error
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

    updated_heat_maps = update_heat_maps(response)

    assert len(study.heat_maps) == len(updated_heat_maps)
