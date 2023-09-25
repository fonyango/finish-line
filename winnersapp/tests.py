import pandas as pd
from django.test import TestCase
from .profiles import DataExtractor
from helpers.utils import Starter

starter = Starter()
db = starter.set_up_database()

class DataExtractionTestCase(TestCase):

    def setUp(self):
        """
        Set up the args for the tests
        """
        self.data_extractor = DataExtractor(db)
        self.athleteID = "S3eOo9"
        self.non_existing_athleteID = "o9"
        self.marathonID = "OhbVrpoiVg"
        self.non_existing_marathon_id = "BB"

    def test_get_athlete_profile_data(self):
        """
        Test if the result is a dataframe
        """
        result = self.data_extractor.get_athletes_profile_data(self.athleteID)
        self.assertIsInstance(result, pd.DataFrame)

    def test_columns_in_get_athlete_profile_data(self):
        """
        Check if all the columns were returned
        """
        required_columns = ['athleteID', 'name', 'gender', 'country', 'raceName', 'marathonID',
                            'year', 'timeTaken', 'worldRecord', 'marathonName']
        result = self.data_extractor.get_athletes_profile_data(self.athleteID)
        self.assertTrue(set(result.columns).issubset(required_columns))

    def test_empty_athlete_profile_data(self):
        """
        Test if the result is empty
        """
        result = self.data_extractor.get_athletes_profile_data(self.non_existing_athleteID)
        self.assertTrue(result.empty)

    def test_get_marathon_profile_data(self):
        """
        Test if the result is a dataframe
        """
        result = self.data_extractor.get_marathon_profile_data(self.marathonID)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_columns_in_get_marathon_profile_data(self):
        """
        Check if all the columns were returned
        """
        required_columns = ['marathonName', 'marathonID', 'raceName', 'athleteID', 
                            'year', 'name','country']
        result = self.data_extractor.get_marathon_profile_data(self.marathonID)
        self.assertTrue(set(result.columns).issubset(required_columns))

    def test_empty_marathon_profile_data(self):
        """
        Test if the result is empty
        """
        result = self.data_extractor.get_marathon_profile_data(self.non_existing_athleteID)
        self.assertTrue(result.empty)

    def test_get_country_performance_data(self):
        """
        Test if the result is a dataframe
        """
        result = self.data_extractor.get_country_performance_data()
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_columns_in_country_performance_data(self):
        """
        Check if all the columns were returned
        """
        required_columns = ['marathonName', 'marathonID', 'raceName', 
        'athleteID', 'year', 'name','country']
        result = self.data_extractor.get_country_performance_data()
        self.assertTrue(set(result.columns).issubset(required_columns))


        