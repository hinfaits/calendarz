import os
import sys
import logging

from flask import Flask, render_template, url_for, request, redirect, abort, Response

from calendarz import config
from calendarz import http_error_handlers
from calendarz import sources
from calendarz import utils
from calendarz.calendar import Calendar
from calendarz.forms import NewForm, EditForm

reload(sys)  
sys.setdefaultencoding('utf8')

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.before_first_request
def setup():
	# Serves nice errors for all exceptions
    http_error_handlers.register_all(app)


@app.route('/', methods=["GET", "POST"])
def home():
    form = NewForm(request.form)
    if request.method == "POST" and form.validate():
        if form.source_type.data == 'csv':
            source = sources.CsvSource(url=form.url.data)
        elif form.source_type.data == 'json':
            source = sources.JsonSource(url=form.url.data)
        elif form.source_type.data == 'google_sheets':
            source = sources.GoogleSheetsSource(url=form.url.data)
        source.put()
        calendar = Calendar.new()
        calendar.source = source.key
        calendar.put()
        ics_url = url_for("render_ics", cal_id=calendar.key.id(), method="ics")
        log_url = url_for("render_ics", cal_id=calendar.key.id(), method="log")
        return render_template("home.html",
                               ics_url=ics_url,
                               log_url=log_url,
                               form=NewForm(dict()))
    else:
        return render_template("home.html", form=form)


@app.route('/calendar/<cal_id>/edit/<secret>')
def edit_calendar(cal_id, secret):
    try:
        calendar = Calendar.get_by_id(cal_id)
        if not calendar.check_secret(secret):
            abort(403)
        return render_template("base.html")
    except AttributeError:
        abort(404)


@app.route('/calendar/<cal_id>/<method>')
def render_ics(cal_id, method):
    calendar = Calendar.get(cal_id)
    if calendar:
        if method == "ics":
            ics, log = calendar.serve_ics()
            filename = "{}.ics".format(calendar.key.id())
            return Response(ics,
                            mimetype="text/calendar", 
                            headers={"Content-Disposition":
                                     "attachment;filename={}".format(filename)})
        elif method == "log":
            ics, log = calendar.serve_ics(flush_cache=True)
            ics_url = url_for("render_ics", cal_id=calendar.key.id(), method="ics")
            return render_template("log.html", log=log, ics_url=ics_url)


@app.route('/about')
def about():
    abort(404)
