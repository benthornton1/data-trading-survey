from datetime import date, timedelta

from flask import url_for
from flask_login import current_user

from app import db
from app.models import (
    HeatMap,
    CardSet,
    Response,
    Card,
    Admin,
    Participant,
    UserGroup,
    DataValueLabel,
    Study,
)
from app.responses.parsing.find_combinations import find_combinations
from app.responses.parsing.update_heat_maps import update_heat_maps


def api_login(client, username="admin", password="password"):
    response = client.post(
        url_for("api.login"), json=dict(username=username, password=password)
    )

    assert response.status_code == 200
    assert "access_token" in response.json

    return response.json


def login(client, username="participant", password="password"):
    response = client.post(
        url_for("auth.login"),
        json=dict(username=username, password=password),
        follow_redirects=True,
    )
    assert response.status_code == 200


def create_admin(client, username="admin", password="password"):
    with client.application.test_request_context():
        admin = Admin(username=username)
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        return admin


def create_participant(
    client,
    username="participant",
    password="password",
    email="test@test.com",
    gender=None,
    age_group=None,
    country_of_birth=None,
    latest_country=None,
    education_level=None,
    occupation=None,
    completed_form=False,
    completed_study=False,
):
    with client.application.test_request_context():
        participant = Participant(
            username=username,
            email=email,
            gender=gender,
            age_group=age_group,
            country_of_birth=country_of_birth,
            latest_country=latest_country,
            education_level=education_level,
            occupation=occupation,
            completed_form=completed_form,
            completed_study=completed_study,
        )
        participant.set_password(password)

        db.session.add(participant)
        db.session.commit()

        return participant


def create_study(
    client,
    name="Test Study",
    description="",
    image="",
    data_values=0,
    number_of_columns=4,
    number_of_rows=4,
    start_date=date.today(),
    end_date=date.today() + timedelta(days=3),
    mail_sent=False,
    creator=None,
    user_group=None,
    card_set_x=None,
    card_set_y=None,
    data_value_labels=None,
):
    with client.application.test_request_context():
        if not creator:
            creator = create_admin(client)
        if not user_group:
            user_group = create_user_group(client, creator=creator)
        if not card_set_x:
            card_set_x = create_card_set(client, creator=creator)
        if not card_set_y:
            card_set_y = create_card_set(client, creator=creator)
        if not data_value_labels:
            data_value_labels = [
                create_data_value_label(client, creator=creator)
            ]
        study = Study(
            name=name,
            description=description,
            image=image,
            data_values=data_values,
            number_of_columns=number_of_columns,
            number_of_rows=number_of_rows,
            start_date=start_date,
            end_date=end_date,
            mail_sent=mail_sent,
            creator=creator,
            user_group=user_group,
            card_set_x=card_set_x,
            card_set_y=card_set_y,
            data_value_labels=data_value_labels,
        )
        db.session.add(study)
        db.session.commit()

        return study


def create_user_group(
    client, name="Test User Group", creator=None, study=None, participants=None
):
    with client.application.test_request_context():
        if not creator:
            creator = create_admin(client)
        if not participants:
            participants = [create_participant(client)]
        user_group = UserGroup(
            name=name, creator=creator, study=study, users=participants
        )
        db.session.add(user_group)
        db.session.commit()

        return user_group


def create_data_value_label(
    client, label="Test Data Value Label", creator=None
):
    with client.application.test_request_context():
        if not creator:
            creator = create_admin(client)
        data_value_label = DataValueLabel(label=label, creator=creator)

        db.session.add(data_value_label)
        db.session.commit()

        return data_value_label


def create_card_set(
    client,
    creator=None,
    cards=None,
    name="Test Card Set",
    measure="Sensitvity",
):
    with client.application.test_request_context():
        if not creator:
            creator = create_admin(client)
        if not cards:
            cards = create_cards(client, creator=creator)
        card_set = CardSet(
            name=name, measure=measure, creator=creator, cards=cards
        )
        db.session.add(card_set)
        db.session.commit()

        return card_set


def create_cards(
    client, creator=None, name="Test Card", description="", image=""
):
    with client.application.test_request_context():
        if not creator:
            creator = create_admin(client)
        card1 = Card(
            name="Entertainment",
            description="Music/ Video/ TV",
            image="yay.jpg",
            creator=creator,
        )
        card2 = Card(
            name="Sensitive Health Report",
            description="Blood Report/ Fertility Test/ DNA Test",
            image="yay.jpg",
            creator=creator,
        )
        card3 = Card(
            name="Activity and Sleep",
            description="",
            image="yay.jpg",
            creator=creator,
        )
        card4 = Card(
            name="Demographics Data",
            description="Age, Gender, Political Opinions, Religion, Height, Weight etc",
            image="yay.jpg",
            creator=creator,
        )
        card5 = Card(
            name="Household",
            description="Energy/ water consumption. Fridge/ Food Cabinet",
            image="yay.jpg",
            creator=creator,
        )
        card6 = Card(
            name="Service Contracts",
            description="Gym/ Telephone/ Mobile/ Internet/ TV",
            image="yay.jpg",
            creator=creator,
        )
        card7 = Card(
            name="GP Health Records",
            description="",
            image="yay.jpg",
            creator=creator,
        )
        card8 = Card(
            name="Fashion",
            description="Wardrobe/ Outfits",
            image="yay.jpg",
            creator=creator,
        )
        card9 = Card(
            name="Communications",
            description="Calls/ Messages/ Chats",
            image="yay.jpg",
            creator=creator,
        )
        card10 = Card(
            name="Financial",
            description="Bank Statements/ Contracts/ Life Insurance/ Vehicle/ Property",
            image="yay.jpg",
            creator=creator,
        )
        card11 = Card(
            name="Food and Beverage",
            description="",
            image="yay.jpg",
            creator=creator,
        )
        card12 = Card(
            name="Location", description="", image="yay.jpg", creator=creator
        )

        card13 = Card(
            name="Mortgage", description="", image="hi.jpg", creator=creator
        )
        card14 = Card(
            name="Research Institute",
            description="",
            image="hi.jpg",
            creator=creator,
        )
        card15 = Card(
            name="Products and Services",
            description="",
            image="hi.jpg",
            creator=creator,
        )
        card16 = Card(
            name="Insurance",
            description="Car insurers, Home insurers",
            image="hi.jpg",
            creator=creator,
        )
        card17 = Card(
            name="Education Institute",
            description="",
            image="hi.jpg",
            creator=creator,
        )
        card18 = Card(
            name="Government Regulated",
            description="Royal Mail, Network Rail",
            image="hi.jpg",
            creator=creator,
        )
        card19 = Card(
            name="Social Media",
            description="Facebook, Snapchat, Instagram, Twitter, etc",
            image="hi.jpg",
            creator=creator,
        )
        card20 = Card(
            name="Health Service",
            description="NHS",
            image="hi.jpg",
            creator=creator,
        )
        card21 = Card(
            name="Religious Organisation",
            description="",
            image="hi.jpg",
            creator=creator,
        )
        card22 = Card(
            name="Supermarket",
            description="Tesco, Sainsburys, Lidl, etc",
            image="hi.jpg",
            creator=creator,
        )
        card23 = Card(
            name="Authorities",
            description="Police",
            image="hi.jpg",
            creator=creator,
        )
        card24 = Card(
            name="Council",
            description="i.e. Cardiff City Council",
            image="hi.jpg",
            creator=creator,
        )
        card25 = Card(
            name="Banks",
            description="i.e. Cardiff City Council",
            image="hi.jpg",
            creator=creator,
        )
        card26 = Card(
            name="Government", description="", image="hi.jpg", creator=creator
        )
        card27 = Card(
            name="Electricity",
            description="Electricity Companies",
            image="hi.jpg",
            creator=creator,
        )
        db.session.add(card1)
        db.session.add(card2)
        db.session.add(card3)
        db.session.add(card4)
        db.session.add(card5)
        db.session.add(card6)
        db.session.add(card7)
        db.session.add(card8)
        db.session.add(card9)
        db.session.add(card10)
        db.session.add(card11)
        db.session.add(card12)
        db.session.add(card13)
        db.session.add(card14)
        db.session.add(card15)
        db.session.add(card16)
        db.session.add(card17)
        db.session.add(card18)
        db.session.add(card19)
        db.session.add(card20)
        db.session.add(card21)
        db.session.add(card22)
        db.session.add(card23)
        db.session.add(card24)
        db.session.add(card25)
        db.session.add(card26)
        db.session.add(card27)
        db.session.commit()

        return [
            card1,
            card2,
            card3,
            card4,
            card5,
            card6,
            card7,
            card8,
            card9,
            card10,
            card11,
            card12,
            card13,
            card14,
            card15,
            card16,
            card17,
            card18,
            card19,
            card20,
            card21,
            card22,
            card23,
            card24,
            card25,
            card26,
            card27,
        ]


def create_card(
    client,
    creator=None,
    name="Test Card",
    description="Test description",
    image="yay.jpg",
):
    with client.application.test_request_context():
        if not creator:
            creator = create_admin(client)
        card = Card(
            name=name, description=description, image=image, creator=creator
        )
        db.session.add(card)
        db.session.commit()
        return card


def create_response(
    client,
    cards_x=None,
    cards_y=None,
    data_values=None,
    participant=None,
    creator=None,
    study=None,
):
    with client.application.test_request_context():
        if not participant:
            participant = create_participant(client)
        if not creator:
            creator = create_admin(client)
        if not cards_x:
            cards_x = {
                "col_0": [
                    {
                        "id": 10,
                        "name": "Financial",
                        "image": "yay.jpg",
                        "description": "Bank Statements/ Contracts/ Life Insurance/ Vehicle/ Property",
                    },
                    {
                        "id": 8,
                        "name": "Fashion",
                        "image": "yay.jpg",
                        "description": "Wardrobe/ Outfits",
                    },
                    {
                        "id": 11,
                        "name": "Food and Beverage",
                        "image": "yay.jpg",
                        "description": "",
                    },
                    {
                        "id": 7,
                        "name": "GP Health Records",
                        "image": "yay.jpg",
                        "description": "",
                    },
                ],
                "col_1": [
                    {
                        "id": 9,
                        "name": "Communications",
                        "image": "yay.jpg",
                        "description": "Calls/ Messages/ Chats",
                    },
                    {
                        "id": 6,
                        "name": "Service Contracts",
                        "image": "yay.jpg",
                        "description": "Gym/ Telephone/ Mobile/ Internet/ TV",
                    },
                    {
                        "id": 12,
                        "name": "Location",
                        "image": "yay.jpg",
                        "description": "",
                    },
                ],
                "col_2": [
                    {
                        "id": 4,
                        "name": "Demographics Data",
                        "image": "yay.jpg",
                        "description": "Age, Gender, Political Opinions, Religion, Height, Weight etc",
                    },
                    {
                        "id": 3,
                        "name": "Activity and Sleep",
                        "image": "yay.jpg",
                        "description": "",
                    },
                    {
                        "id": 5,
                        "name": "Household",
                        "image": "yay.jpg",
                        "description": "Energy/ water consumption. Fridge/ Food Cabinet",
                    },
                ],
                "col_3": [
                    {
                        "id": 1,
                        "name": "Entertainment",
                        "image": "yay.jpg",
                        "description": "Music/ Video/ TV",
                    },
                    {
                        "id": 2,
                        "name": "Sensitive Health Report",
                        "image": "yay.jpg",
                        "description": "Blood Report/ Fertility Test/ DNA Test",
                    },
                ],
            }
        if not cards_y:
            cards_y = {
                "row_3": [
                    {
                        "id": 18,
                        "name": "Government Regulated",
                        "image": "hi.jpg",
                        "description": "Royal Mail, Network Rail",
                    },
                    {
                        "id": 13,
                        "name": "Mortgage",
                        "image": "hi.jpg",
                        "description": "",
                    },
                    {
                        "id": 25,
                        "name": "Banks",
                        "image": "hi.jpg",
                        "description": "",
                    },
                    {
                        "id": 22,
                        "name": "Supermarket",
                        "image": "hi.jpg",
                        "description": "Tesco, Sainsburys, Lidl, etc",
                    },
                    {
                        "id": 15,
                        "name": "Products and Services",
                        "image": "hi.jpg",
                        "description": "",
                    },
                ],
                "row_2": [
                    {
                        "id": 16,
                        "name": "Insurance",
                        "image": "hi.jpg",
                        "description": "Car insurers, Home insurers",
                    },
                    {
                        "id": 14,
                        "name": "Research Institute",
                        "image": "hi.jpg",
                        "description": "",
                    },
                    {
                        "id": 27,
                        "name": "Electricity",
                        "image": "hi.jpg",
                        "description": "Electricity Companies",
                    },
                    {
                        "id": 26,
                        "name": "Government",
                        "image": "hi.jpg",
                        "description": "",
                    },
                    {
                        "id": 24,
                        "name": "Council",
                        "image": "hi.jpg",
                        "description": "i.e. Cardiff City Council",
                    },
                ],
                "row_1": [
                    {
                        "id": 20,
                        "name": "Health Service",
                        "image": "hi.jpg",
                        "description": "NHS",
                    },
                    {
                        "id": 21,
                        "name": "Religious Organisation",
                        "image": "hi.jpg",
                        "description": "",
                    },
                    {
                        "id": 17,
                        "name": "Education Institute",
                        "image": "hi.jpg",
                        "description": "",
                    },
                ],
                "row_0": [
                    {
                        "id": 19,
                        "name": "Social Media",
                        "image": "hi.jpg",
                        "description": "Facebook, Snapchat, Instagram, Twitter, etc",
                    },
                    {
                        "id": 23,
                        "name": "Authorities",
                        "image": "hi.jpg",
                        "description": "Police",
                    },
                ],
            }
        if not data_values:
            data_values = {
                "col_0_row_3": [
                    {"id": 1, "label": "Test Data Value Label", "value": 43},
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 63,
                    },
                ],
                "col_1_row_3": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 82,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 72,
                    },
                ],
                "col_2_row_3": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 82,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 99,
                    },
                ],
                "col_3_row_3": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 71,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 72,
                    },
                ],
                "col_0_row_2": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 42,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 52,
                    },
                ],
                "col_1_row_2": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 67,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 89,
                    },
                ],
                "col_2_row_2": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 52,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 62,
                    },
                ],
                "col_3_row_2": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 66,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 72,
                    },
                ],
                "col_0_row_1": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 82,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 65,
                    },
                ],
                "col_1_row_1": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 82,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 32,
                    },
                ],
                "col_2_row_1": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 42,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 82,
                    },
                ],
                "col_3_row_1": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 92,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 73,
                    },
                ],
                "col_0_row_0": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 43,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 77,
                    },
                ],
                "col_1_row_0": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 28,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 32,
                    },
                ],
                "col_2_row_0": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 12,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 44,
                    },
                ],
                "col_3_row_0": [
                    {
                        "id": 1,
                        "label": "You get the benefit (e.g. Personalised Service)",
                        "value": 66,
                    },
                    {
                        "id": 2,
                        "label": "Data Consumer gets the benefit (e.g. Supply Chain gets the benefit)",
                        "value": 34,
                    },
                ],
            }
        response = Response(
            cards_x=cards_x,
            cards_y=cards_y,
            data_values=data_values,
            creator=creator,
            participant=participant,
            study=study,
        )
        db.session.add(response)
        db.session.commit()

        return response


def create_heat_maps(client, creator=None, study=None, responses=None):
    with client.application.test_request_context():
        if not creator:
            creator = create_admin(client)
        if not study:
            study = create_study(client, creator=creator)
        if responses is None:
            responses = [create_response(client, creator=creator)]
        find_combinations(study)
        for response in responses:
            update_heat_maps(response)
        heat_maps = HeatMap.query.filter_by(study=study).all()

        return heat_maps
