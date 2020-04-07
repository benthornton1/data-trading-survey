from datetime import date, timedelta
import random
import string

from flask import current_app
from flask_mail import Message
from flask.templating import render_template
from sqlalchemy import func

from app import mail, db
from app.models import Study, UserGroup
from tests.helpers import create_admin, create_participant, create_study, create_user_group

def test_send_mail(client, init_database):
    """
    GIVEN a Flask application, admin, study
    WHEN study is today
    THEN check emails are sent with correct content
    """
    with client.application.test_request_context():
        
        admin=create_admin(client, username='admin', password='password')
        participant_1 = create_participant(client, username='p1')
        participant_2 = create_participant(client, username='p2')
        participant_3 = create_participant(client, username='p3')
        participant_4 = create_participant(client, username='p4')
        participant_5 = create_participant(client, username='p5')
        
        user_group = create_user_group(client, creator=admin, participants=[participant_1, participant_2])
        user_group_2 = create_user_group(client, creator=admin, participants=[participant_3, participant_4, participant_5])
        study = create_study(client, start_date=date.today(), creator=admin, user_group=user_group)
        study2 = create_study(client, creator=admin, start_date=date.today()+timedelta(days=3))
        study_3 = create_study(client, creator=admin, start_date=date.today(), user_group=user_group_2)
        
        studies = Study.query.filter(func.DATE(Study.start_date)==date.today()).all()
        assert study2 not in studies
        
        letters = string.ascii_letters
        strength = 8
        for study in studies:
            if study.mail_sent == False:
                user_group = UserGroup.query.filter_by(id=study.user_group_id).first()
                if user_group:
                    with mail.record_messages() as outbox:

                        for user in user_group.users:
                            password = ''.join(random.choice(letters) for i in range(strength))
                            user.set_password(password)
                            body = render_template('email.html', study=study, username=user.username, password=password)
                            
                            msg = Message("You Have Been Invited To A Study!",
                                        recipients=[user.email],
                                        sender=current_app.config['MAIL_USERNAME']        
                                        )
                            msg.html=body
                            
                            assert password in msg.html
                            assert user.username in msg.html
                            assert msg.recipients[0] == user.email
                        
                            mail.send(msg)
                            user.email = None
                            assert user.email is None
                        assert len(outbox) == len(user_group.users)
                        
            
                try:
                    study.mail_sent = True
                    db.session.commit()
                except:
                    db.session.rollback()
    