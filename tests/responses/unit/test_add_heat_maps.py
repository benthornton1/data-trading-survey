from app.responses.parsing.add_heat_maps import (
    CreateAllHeatMaps,
    CreateOneHeatMap,
)
from app.responses.parsing.find_combinations import find_combinations
from app.responses.parsing.update_heat_maps import update_heat_maps
from tests.helpers import (
    create_admin,
    create_data_value_label,
    create_participant,
    create_response,
    create_study,
    create_user_group,
)


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

    # No label
    find_combinations(study)
    update_heat_maps(response)
    c = CreateOneHeatMap()
    c.add(
        is_count=False,
        study=study,
        card_x_id=study.card_set_x.cards[0].id,
        card_y_id=study.card_set_y.cards[1].id,
    )
    plot = c.plots

    assert isinstance(plot, list)
    assert isinstance(plot[0], tuple)
    assert len(plot) == 1

    c.add(
        is_count=True,
        study=study,
        card_x_id=study.card_set_x.cards[0].id,
        card_y_id=study.card_set_y.cards[1].id,
    )
    plot = c.plots

    assert isinstance(plot, list)
    assert isinstance(plot[0], tuple)
    assert len(plot) == 1

    # with label
    participant_2 = create_participant(client, username="p2")
    user_group = create_user_group(
        client, participants=[participant_2], creator=admin
    )
    study_2 = create_study(client, creator=admin, user_group=user_group)
    response = create_response(
        client, study=study, creator=admin, participant=participant_2
    )

    find_combinations(study_2)
    update_heat_maps(response)
    c = CreateOneHeatMap()
    c.add(
        is_count=False,
        study=study_2,
        card_x_id=study_2.card_set_x.cards[0].id,
        card_y_id=study_2.card_set_y.cards[1].id,
        label=study_2.data_value_labels[0],
    )
    plot = c.plots

    assert isinstance(plot, list)
    assert isinstance(plot[0], tuple)
    assert len(plot) == 1

    c.add(
        is_count=True,
        study=study_2,
        card_x_id=study_2.card_set_x.cards[0].id,
        card_y_id=study_2.card_set_y.cards[1].id,
    )
    plot = c.plots

    assert isinstance(plot, list)
    assert isinstance(plot[0], tuple)
    assert len(plot) == 1


def test_CreateAllHeatMaps(client, init_database):
    """
    GIVEN a Flask application, study, response
    WHEN CreateAllHeatMaps.add is called 
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

    # No label
    find_combinations(study)
    update_heat_maps(response)
    c = CreateAllHeatMaps()
    c.add(is_count=False, study=study)
    plots = c.plots

    assert isinstance(plots, list)
    assert isinstance(plots[0], tuple)
    assert len(plots) == len(study.card_set_x.cards) * len(
        study.card_set_y.cards
    ) * len(study.data_value_labels)

    c.add(is_count=True, study=study)
    plots = c.plots

    assert isinstance(plots, list)
    assert isinstance(plots[0], tuple)
    assert len(plots) == len(study.card_set_x.cards) * len(
        study.card_set_y.cards
    ) * len(study.data_value_labels)

    # with label
    participant_2 = create_participant(client, username="p2")
    user_group = create_user_group(
        client, participants=[participant_2], creator=admin
    )
    study_2 = create_study(client, creator=admin, user_group=user_group)
    response = create_response(
        client, study=study, creator=admin, participant=participant_2
    )

    find_combinations(study_2)
    update_heat_maps(response)
    c = CreateAllHeatMaps()
    c.add(is_count=False, study=study_2)
    plots = c.plots

    assert isinstance(plots, list)
    assert isinstance(plots[1], tuple)
    assert len(plots) == len(study_2.card_set_x.cards) * len(
        study_2.card_set_y.cards
    ) * len(study_2.data_value_labels)

    c.add(is_count=True, study=study_2)
    plots = c.plots

    assert isinstance(plots, list)
    assert isinstance(plots[1], tuple)
    assert len(plots) == len(study_2.card_set_x.cards) * len(
        study_2.card_set_y.cards
    ) * len(study_2.data_value_labels)
