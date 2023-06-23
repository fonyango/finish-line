import pandas as pd
import numpy as np

def get_athletes_summary(data):
    total_athletes = data['AthleteID'].nunique()
    summary_df = data.groupby('Race').agg(
        num_athletes=('AthleteID',pd.Series.nunique)).reset_index()
    
    race_summary_list = summary_df.to_dict('records')
    race_summary = {item['Race']: item['num_athletes'] for item in race_summary_list}
    race_summary['totalAthletes'] = total_athletes

    return race_summary

