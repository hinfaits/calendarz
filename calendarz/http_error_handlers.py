from flask import request, render_template, Markup
from werkzeug.exceptions import default_exceptions


def register_all(app):
    """
    Register handler() to print all error pages for `app`
    """
    for err in default_exceptions:
        app.register_error_handler(err, handler)


def handler(error):
    """
    Build pretty error pages
    """
    return render_template("error.html",
                           code=error.code,
                           name=error.name,
                           description=Markup(error.description)), error.code
