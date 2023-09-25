import pandas as pd
import numpy as np
from helpers.utils import Starter

# Instatiate Starter class
starter = Starter()

class DataExtractor():

    def __init__(self,db):

        self.db = db

    def get_athletes_profile_data(self,athleteID):
        

        # athletes data
        query = {"athleteID":1,"name":1,"gender":1, "country":1}
        filter_query = {"athleteID":athleteID}
        athletes = self.db["athletes"]
        athletes_df = starter.mongo_to_dataframe(list(athletes.find(filter_query,query)))

        if athletes_df.empty==True:
            
            profile_df = pd.DataFrame()

            return profile_df

        else:
            # races data
            query = {"raceName":1,"athleteID":1,"marathonID":1,"timeTaken":1,"year":1,"worldRecord":1}
            races = self.db["races"]
            races_df = starter.mongo_to_dataframe(list(races.find(filter_query,query)))

            # marathons data
            query = {"marathonID":1,'marathonName':1}
            marathon_ids = races_df['marathonID'].to_list()
            filter_query = {"marathonID":{"$in":marathon_ids}}
            marathons = self.db["marathons"]
            marathon_df = starter.mongo_to_dataframe(list(marathons.find(filter_query,query)))

            # merge the data
            profile_df = athletes_df.merge(races_df, on="athleteID",how='left')
            profile_df = profile_df.merge(marathon_df, on='marathonID',how='left')

            columns_to_drop = profile_df.filter(like='_id').columns
            profile_df = profile_df.drop(columns=columns_to_drop)
        
        return profile_df

    def get_marathon_profile_data(self, marathonID):

        # marathons data
        query = {"marathonID":1,'marathonName':1}
        filter_query = {"marathonID":marathonID}
        marathons = self.db["marathons"]
        marathon_df = starter.mongo_to_dataframe(list(marathons.find(filter_query,query)))

        if marathon_df.empty==True:

            return pd.DataFrame()

        else:

            # races data
            query = {"raceName":1,"athleteID":1,"marathonID":1,"year":1}
            marathon_ids = marathon_df['marathonID'].to_list() 
            filter_query = {"marathonID":{"$in":marathon_ids}}
            races = self.db["races"]
            races_df = starter.mongo_to_dataframe(list(races.find(filter_query,query)))


            # athletes data
            query = {"athleteID":1,"name":1,"country":1}
            athlete_ids = races_df['athleteID'].to_list()
            filter_query = {"athleteID":{"$in":athlete_ids}}
            athletes = self.db["athletes"]
            athletes_df = starter.mongo_to_dataframe(list(athletes.find(filter_query,query)))

            # merge the data
            combined_df = marathon_df.merge(races_df, on="marathonID",how='left')
            combined_df = combined_df.merge(athletes_df, on='athleteID',how='left')

            columns_to_drop = combined_df.filter(like='_id').columns
            combined_df = combined_df.drop(columns=columns_to_drop)

        return combined_df

    def get_country_performance_data(self):
        # marathons data
        query = {"marathonID":1,'marathonName':1}
        marathons = self.db["marathons"]
        marathon_df = starter.mongo_to_dataframe(list(marathons.find({},query)))

        if marathon_df.empty==True:
            return pd.DataFrame()

        else:
            # races data
            query = {"raceName":1,"athleteID":1,"marathonID":1,"year":1}
            marathon_ids = marathon_df['marathonID'].to_list() 
            filter_query = {"marathonID":{"$in":marathon_ids}}
            races = self.db["races"]
            races_df = starter.mongo_to_dataframe(list(races.find(filter_query,query)))

            # athletes data
            query = {"athleteID":1,"name":1,"country":1}
            athlete_ids = races_df['athleteID'].to_list()
            filter_query = {"athleteID":{"$in":athlete_ids}}
            athletes = self.db["athletes"]
            athletes_df = starter.mongo_to_dataframe(list(athletes.find(filter_query,query)))

            # merge the data
            combined_df = marathon_df.merge(races_df, on="marathonID",how='left')
            combined_df = combined_df.merge(athletes_df, on='athleteID',how='left')

            columns_to_drop = combined_df.filter(like='_id').columns
            combined_df = combined_df.drop(columns=columns_to_drop)

        return combined_df

class Marathons():

    def __init__(self,data):
        """
        Initializes the Marathons class with the provided data.

        Args:
            data (pandas.DataFrame): The input data containing marathon winners' information.
        """
        self.data = data 

    def get_athletes_profile(self):
        """
        Provides the athlete's profile

        Returns:
            dict: A dictionary containing the number of athletes in each race and the total number of unique athletes.
        """

        athlete_name = self.data['name'].drop_duplicates().tolist()[0]
        gender = self.data['gender'].drop_duplicates().tolist()[0]
        country = self.data['country'].drop_duplicates().tolist()[0]
        race = self.data['raceName'].drop_duplicates().tolist()[0]
        num_wins = self.data['raceName'].count()
        num_marathons = self.data['marathonID'].nunique()
        fastest_time = self.data['timeTaken'].min()
        first_win = self.data['year'].min()
        last_win = self.data['year'].max()

        result = {
            "name":athlete_name,
            "gender":gender,
            "country":country,
            "race":race,
            "num_wins":num_wins,
            "num_marathons":num_marathons,
            "best_time":fastest_time,
            "first_win":first_win,
            "last_win":last_win
        }

        return result

    def get_marathons_summary(self):
        """
        Generate a summary of marathons, including the number of winners, unique countries, and unique years for each marathon.

        Returns:
            list of dict: A list of dictionaries, each containing summary information for a marathon.
        """

        marathon_name = self.data['marathonName'].drop_duplicates().tolist()[0]
        num_races = self.data['raceName'].nunique()
        num_countries = self.data['country'].nunique()
        first_time = self.data['year'].min()
        last_time = self.data['year'].max()

        result = {
            "name":marathon_name,
            "num_countries":num_countries,
            "num_races":num_races,
            "first_time":first_time,
            "last_time":last_time
        }

        return result

    
    def get_country_summary(self):
        """
        Generate a summary of country performance

        Returns:
            list of dict: A list of dictionaries for each country
        """

        country_df = self.data.groupby(['country','marathonName','raceName']).agg(
                        num_athletes=('athleteID', np.size)
                    ).reset_index()

        result = country_df.to_dict('records')

        return result
        