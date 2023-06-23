import pandas as pd
import numpy as np


class Marathons():

    def __init__(self,data):
        self.data = data 

    def get_athletes_summary(self):

        total_athletes = self.data['AthleteID'].nunique()
        summary_df = self.data.groupby('Race').agg(
            num_athletes=('AthleteID',pd.Series.nunique)).reset_index()
        
        race_summary_list = summary_df.to_dict('records')
        race_summary = {item['Race']: item['num_athletes'] for item in race_summary_list}
        race_summary['totalAthletes'] = total_athletes

        return race_summary

    def get_marathons_summary(self):
        
        num_marathons = self.data['Marathon'].nunique()
        marathons_summary = self.data.groupby(['Marathon','Race']).agg(
                    num_winners=('AthleteID',pd.Series.nunique),
                    num_countries=('Country',pd.Series.nunique),
                    num_years=('Year',pd.Series.nunique)
                    ).reset_index()
        
        marathons_summary_list = marathons_summary.to_dict('records')

        return marathons_summary_list 
        