import hashlib
import os
import urllib.parse

from flask import url_for, current_app, render_template, request
from flask_login import current_user
from munch import munchify
import pdfkit
from sqlalchemy.orm import session

from app.models import Response
from app.responses.parsing.average_response2 import average_response as ggh


def create_pdf(
    study, all_responses=False, average_response2=False, response_ids=False
):
    average_response_pdf = None
    responses_pdf = []
    if average_response2 == True:
        average_response_pdf = munchify(ggh(study))
    if all_responses == True:
        responses_pdf = study.responses
    if response_ids != False:
        responses = (
            Response.query.filter(Response.id.in_(response_ids))
            .filter(Response.study_id == study.id)
            .all()
        )
        responses_pdf = responses

    html = render_template(
        "responses/response.html",
        study=study,
        card_set_x=study.card_set_x,
        card_set_y=study.card_set_y,
        average_response=average_response_pdf,
        responses=responses_pdf,
    )
    file_name = (
        str(
            int(hashlib.sha256(html.encode("utf-8")).hexdigest(), 16) % 10 ** 8
        )
        + ".pdf"
    )
    file_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        "pdf",
        str(study.creator.id),
        file_name,
    )
    html_file_path = os.path.join(
        url_for("static", filename="pdf"), str(study.creator.id), file_name
    )

    if os.path.exists(file_path):
        return html_file_path
    else:
        options = {'page-size': 'A3'}
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        css_bootstrap = os.path.abspath("app/static/css/bootstrap/bootstrap.min.css")
        css_local = os.path.abspath("app/static/css/board.css")
        pdfkit.from_string(html, file_path, css=[css_bootstrap, css_local], options=options)

        return html_file_path
