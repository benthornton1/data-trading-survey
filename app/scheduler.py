from app import scheduler, db, mail
from flask import current_app
from app.models import Study, UserGroup
from datetime import date
from sqlalchemy import func
import string, random
from flask_mail import Message

 
@scheduler.task('cron', id='do_start_study_job', hour=0, minute=5)
def start_study_job():
    print('hello')
    # # print(type(date.today()))
    studies = Study.query.filter(func.DATE(Study.start_date)==date.today()).all()
    letters = string.ascii_letters
    strength = 6
    
    for study in studies:
        user_group = UserGroup.query.filter_by(id=study.user_group_id).first_or_404()
        # with mail.connect() as conn:
        for user in user_group.users:
            password = ''.join(random.choice(letters) for i in range(strength))
            user.set_password(password)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            # with mail.record_messages() as outbox: 
            msg = Message("You Have Been Invited To A User Study!",
                        recipients=[user.email],
                        sender=current_app.config['ADMINS'][0]        
                        )
            msg.body= "Here is your password for the study {}".format(password)
            # 
            with current_app.app_context():
                mail.send(msg)
            