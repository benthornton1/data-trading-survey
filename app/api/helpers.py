def create_participant_json(user):
    json = {
        "id": user.id,
        "username": user.username,
        "type": user.type,
        "gender": user.gender,
        "age_group": user.age_group,
        "country_of_birth": user.country_of_birth,
        "education_level": user.education_level,
        "occupation": user.occupation,
        "income": user.income,
        "user_group_id": user.user_group_id,
    }
    return json


def create_card_json(card):
    json = {
        "id": card.id,
        "name": card.name,
        "description": card.description,
        "image": card.image,
    }
    return json


def create_card_set_json(card_set):
    json = {
        "id": card_set.id,
        "name": card_set.name,
        "measure": card_set.measure,
        "cards": [create_card_json(card) for card in card_set.cards],
    }
    return json


def create_data_value_label_json(data_value_label):
    json = {
        "id": data_value_label.id,
        "label": data_value_label.label,
        "study_id": data_value_label.study_id,
    }
    return json


def create_study_json(study):
    json = {
        "id": study.id,
        "name": study.name,
        "description": study.description,
        "image": study.image,
        "card_set_x": create_card_set_json(study.card_set_x),
        "card_set_y": create_card_set_json(study.card_set_y),
        "data_value_labels": [
            create_data_value_label_json(data_value_label)
            for data_value_label in study.data_value_labels
        ],
        "number_of_columns": study.number_of_columns,
        "number_of_rows": study.number_of_rows,
        "user_group_id": study.user_group_id,
        "start_date": study.start_date,
        "end_date": study.end_date,
    }

    return json


def create_card_position_json(card_position):
    json = {
        "id": card_position.id,
        "position": card_position.position,
        "card_id": card_position.card_id,
        "response_id": card_position.response_id,
    }
    return json


def create_data_value_json(data_value):
    json = {
        "id": data_value.id,
        "column": data_value.column,
        "row": data_value.row,
        "value": data_value.value,
        "data_value_label_id": data_value.data_value_label_id,
        "response_id": data_value.response_id,
    }
    return json


def create_response_json(response):
    json = {
        "id": response.id,
        "study_id": response.study_id,
        "participant_id": response.participant_id,
        "card_positions": [
            create_card_position_json(card_position)
            for card_position in response.card_positions
        ],
        "data_values": [
            create_data_value_json(data_value) for data_value in response.data_values
        ],
    }
    return json


def create_heat_map_json(heat_map):
    if heat_map.data_value_label:
        json = {
            "id": heat_map.id,
            "card_x": create_card_json(heat_map.card_x),
            "card_y": create_card_json(heat_map.card_y),
            "study_id": heat_map.study_id,
            "values": heat_map.values,
            "data_value_label_id": heat_map.data_value_label.id,
            "is_count": heat_map.is_count,
        }
    else:
        json = {
            "id": heat_map.id,
            "card_x": create_card_json(heat_map.card_x),
            "card_y": create_card_json(heat_map.card_y),
            "study_id": heat_map.study_id,
            "values": heat_map.values,
            "data_value_label_id": None,
            "is_count": heat_map.is_count,
        }

    return json


def create_user_group_json(user_group):
    json = {}
    if user_group.study:
        json = {
            "id": user_group.id,
            "name": user_group.name,
            "users": [create_participant_json(user) for user in user_group.users],
            "study": user_group.study.id,
        }
    else:
        json = {
            "id": user_group.id,
            "name": user_group.name,
            "users": [create_participant_json(user) for user in user_group.users],
            "study": None,
        }

    return json
