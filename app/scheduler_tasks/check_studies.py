from app import scheduler, db, mail
from flask import current_app
from app.models import Study, UserGroup
from datetime import date
from sqlalchemy import func
import string, random
from flask_mail import Message
from app import scheduler

def check_studies(app):
    with app.app_context():
        studies = Study.query.filter(func.DATE(Study.start_date)==date.today()).all()
        letters = string.ascii_letters
        strength = 6
        for study in studies:
            if study.mail_sent == False:
                
                user_group = UserGroup.query.filter_by(id=study.user_group_id).first_or_404()
                
                for user in user_group.users:
                    password = ''.join(random.choice(letters) for i in range(strength))
                    username = ''.join(random.choice(letters) for i in range(strength))
                    user.username = username
                    user.set_password(password)
                    try:
                        db.session.commit()
                    except:
                        db.session.rollback()

                    msg = Message("You Have Been Invited To A User Study!",
                                recipients=[user.email],
                                sender=current_app.config['ADMINS'][0]        
                                )
                    msg.body= "Here is your username for the study: {username}\n"\
                        "Here is your password: {password}".format(username=username,password=password)
                
                    mail.send(msg)
        
                    try:
                        study.mail_sent = True
                        db.session.commit()
                    except:
                        db.session.rollback()
    
    