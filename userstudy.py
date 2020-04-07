from flask import current_app

from app import create_app, db, scheduler
from app.models import Admin, Card, CardSet, Participant, Study, User, UserGroup
from app.scheduler_tasks.check_studies import check_studies


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Admin': Admin, 'Participant': Participant,
            'Study':Study, 'Card':Card, 'CardSet':CardSet, 'UserGroup':UserGroup}
