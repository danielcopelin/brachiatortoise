# -*- coding: utf-8 -*-

from flask import Flask
from app import strava
#import pandas as pd

#import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

app = Flask(__name__)

h5 = 'store.h5'
strava.get_new_activities(h5)

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(
    func=strava.get_new_activities,
    args=[h5],
    trigger=IntervalTrigger(seconds=60*60),
    id='get_new_activiteis',
    name='Get new activities from Strava',
    replace_existing=True)
# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

from app import routes