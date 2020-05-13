import string, random
from datetime import date

from flask import current_app, render_template
from flask_mail import Message
from sqlalchemy import func

from app import scheduler, db, mail
from app.models import Study, UserGroup


def check_studies(app):
    with app.app_context():
        studies = Study.query.filter(func.DATE(Study.start_date) == date.today()).all()
        letters = string.ascii_letters
        strength = 8
        for study in studies:
            if study.mail_sent is False:
                user_group = UserGroup.query.filter_by(id=study.user_group_id).first()
                if user_group:
                    with mail.connect() as conn:

                        for user in user_group.users:
                            password = "".join(
                                random.choice(letters) for i in range(strength)
                            )
                            user.set_password(password)

                            body = render_template(
                                "email.html",
                                study=study,
                                username=user.username,
                                password=password,
                            )
                            msg = Message(
                                "You Have Been Invited To A Study!",
                                recipients=[user.email],
                                sender=current_app.config["MAIL_USERNAME"],
                            )
                            msg.html = body
                            conn.send(msg)
                            user.email = None

                try:
                    study.mail_sent = True
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
