from app import create_app, db, scheduler
from app.scheduler_tasks.check_studies import check_studies
from app.models import User, Study, Card, CardSet, UserGroup

from flask import current_app

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Study':Study, 'Card':Card, 'CardSet':CardSet, 'UserGroup':UserGroup}
