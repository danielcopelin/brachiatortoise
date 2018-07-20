# -*- coding: utf-8 -*-

from app import app, strava
from flask import render_template, send_file
import pandas as pd
from StringIO import StringIO

@app.route('/')
@app.route('/index')
def index():
    with pd.HDFStore('store.h5') as store:
        club_df = store['club_df']
    return render_template("index.html", title='brachiatortoise', table=club_df.to_html())

@app.route('/fig')
def fig():
    with pd.HDFStore('store.h5') as store:
        club_df = store['club_df']
    fig = strava.cumulative_plot(club_df)
    img = StringIO()
    fig.savefig(img)
    img.seek(0)
    return send_file(img, mimetype='image/png')