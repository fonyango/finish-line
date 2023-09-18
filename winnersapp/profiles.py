import pandas as pd
import numpy as np


class Marathons():

    def __init__(self,data):
        """
        Initializes the Marathons class with the provided data.

        Args:
            data (pandas.DataFrame): The input data containing marathon winners' information.
        """
        self.data = data 

    def get_athletes_summary(self):
        """
        Summarizes the number of athletes in each race and provides the total number of unique athletes.

        Returns:
            dict: A dictionary containing the number of athletes in each race and the total number of unique athletes.
        """
        total_athletes = self.data['AthleteID'].nunique()
        summary_df = self.data.groupby('Race').agg(
            num_athletes=('AthleteID',pd.Series.nunique)).reset_index()
        
        race_summary_list = summary_df.to_dict('records')
        race_summary = {item['Race']: item['num_athletes'] for item in race_summary_list}
        race_summary['totalAthletes'] = total_athletes

        return race_summary

    def get_marathons_summary(self):
        """
        Generate a summary of marathons, including the number of winners, unique countries, and unique years for each marathon.

        Returns:
            list of dict: A list of dictionaries, each containing summary information for a marathon.
        """
        num_marathons = self.data['Marathon'].nunique()
        marathons_summary = self.data.groupby(['Marathon','Race']).agg(
                    num_winners=('AthleteID',pd.Series.nunique),
                    num_countries=('Country',pd.Series.nunique),
                    num_years=('Year',pd.Series.nunique)
                    ).reset_index()
        
        marathons_summary_list = marathons_summary.to_dict('records')

        return marathons_summary_list 
        