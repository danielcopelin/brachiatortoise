# -*- coding: utf-8 -*-

from app import app#, strava
from flask import render_template, request#, send_file
# import pandas as pd
# from StringIO import StringIO
from stravalib.client import Client

@app.route('/')
@app.route('/index')
def index():
    client = Client()
    authorize_url = client.authorization_url(client_id=19055, redirect_uri='http://localhost:5000/authorized')
    return render_template("index.html", title='brachiatortoise', authorize_url=authorize_url)

@app.route('/authorized')
def authorized():
    # status = request.status
    try:
        code = request.args.get('code')
        status = 'Successfully logged in!'
    except:
        code = 'null'
        status = 'Login failed.'
    return render_template("authorized.html", title='brachiatortoise', code=code, status=status)

# @app.route('/fig')
# def fig():
#     with pd.HDFStore('store.h5') as store:
#         club_df = store['club_df']
#     fig = strava.cumulative_plot(club_df)
#     img = StringIO()
#     fig.savefig(img)
#     img.seek(0)
#     return send_file(img, mimetype='image/png')