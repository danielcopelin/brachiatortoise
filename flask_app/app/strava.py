# -*- coding: utf-8 -*-

import stravalib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#matplotlib.use('Agg')

def get_new_activities(h5):
    print("Getting new activities...")
    
    with pd.HDFStore(h5) as store:
        df = store['club_df']
    
    client = stravalib.client.Client()
    access_token = ''
    client.access_token = access_token
    # athlete = client.get_athlete()
        
    club_activities = client.get_club_activities(329445)
    for activity in club_activities:
        if activity.start_date_local.year != 2018:
            break
        elif activity.id not in df.index:
            print('\rGetting new activity {0}...'.format(activity.id)),
            act_dict = {}
            act_dict['name'] = activity.name
            act_dict['upload_id'] = activity.upload_id
            act_dict['athlete_id'] = activity.athlete.id
            act_dict['athlete_name'] = '{0} {1}'.format(activity.athlete.firstname, activity.athlete.lastname)
            act_dict['start_date_local'] = activity.start_date_local
            act_dict['moving_time'] = activity.moving_time
            act_dict['distance'] = activity.distance
            act_dict['average_speed'] = activity.average_speed
            act_dict['total_elevation_gain'] = activity.total_elevation_gain
            
            for k, v in act_dict.items():
                df.loc[activity.id, k] = v

    cumulative(df, 'athlete_id', 'distance', 'start_date_local')
    cumulative(df, 'athlete_id', 'total_elevation_gain', 'start_date_local')
    cumulative(df, 'athlete_id', 'moving_time', 'start_date_local')    
    
    with pd.HDFStore(h5) as store:
        store['club_df'] = df
            
def cumulative(df, athlete_field, data_field, date):
    '''Calculates the to-date cumulative sum of the athlete's data for each activity.'''
    for athlete in set(df[athlete_field]):
        temp_df = df.loc[(df[athlete_field] == athlete),[data_field,date]]
        temp_df['id'] = temp_df.index
        temp_df = temp_df.set_index(date, drop=False)
        temp_df = temp_df.sort_index()
        temp_df['cumulative'] = temp_df.loc[:,data_field].cumsum()
        temp_df = temp_df.set_index('id')
        df.loc[df[athlete_field] == athlete,'cumulative_{0}'.format(data_field)] = temp_df['cumulative']
        
def cumulative_plot(df):
    fig, ax = plt.subplots()
    for athlete in set(df['athlete_name']):
        temp_df = df.loc[df['athlete_name'] == athlete,['start_date_local','cumulative_distance']].set_index('start_date_local').sort_index()
        x, y = temp_df.index, temp_df['cumulative_distance'].values
        ax.plot(x,y,label=athlete)
    
    ax.legend()
    fig.autofmt_xdate()
    fig.set_size_inches(20,10)
    
    return fig