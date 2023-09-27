import pandas as pd
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory
from .views import winnersViewset
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


class winnersViewsetTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_athletes_summary(self):
        view = winnersViewset.as_view({'post':'get_athletes_summary'})
        data = {'athlete_id':"S3eOo9"}
        request = self.factory.post('profile/', data)
        response = view(request)
        self.assertEqual(response.data['Status'], status.HTTP_200_OK)
        self.assertEqual(response.data['Success'], True)
        self.assertEqual(response.data['Message'],"Successful")
        
    def test_get_athletes_summary_empty_df(self):
        view = winnersViewset.as_view({'post':'get_athletes_summary'})
        data = {"athlete_id":1} # this id is not there
        request = self.factory.post('profile/',data)
        response = view(request)
        self.assertEqual(response.data['Status'], status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['Success'], False)
        self.assertEqual(response.data['Message'], "No Data Found")

    def test_get_athletes_summary_get(self):
        view = winnersViewset.as_view({'get':'get_athletes_summary'})
        request = self.factory.get('profile/')
        response = view(request)
        self.assertEqual(response.data["Status"], status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['Success'], False)

    def test_get_marathons_profile(self):
        view = winnersViewset.as_view({'post':'get_marathons_profile'})
        data = {'marathon_id':"OhbVrpoiVg"}
        request = self.factory.post('marathon/', data)
        response = view(request)
        self.assertEqual(response.data['Status'], status.HTTP_200_OK)
        self.assertEqual(response.data['Success'], True)
        self.assertEqual(response.data['Message'],"Successful")
     
    def test_get_marathons_profile_empty_df(self):
        view = winnersViewset.as_view({'post':'get_marathons_profile'})
        data = {"marathon_id":1} # this id is not there
        request = self.factory.post('marathon/',data)
        response = view(request)
        self.assertEqual(response.data['Status'], status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['Success'], False)
        self.assertEqual(response.data['Message'], "No Data Found")

    def test_get_marathons_profile_get(self):
        view = winnersViewset.as_view({'get':'get_marathons_profile'})
        request = self.factory.get('marathon/')
        response = view(request)
        self.assertEqual(response.data["Status"], status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['Success'], False)

    def test_get_country_performance(self):
        view = winnersViewset.as_view({'get':'get_country_performance'})
        request = self.factory.get('country-performance/')
        response = view(request)
        self.assertEqual(response.data["Status"], status.HTTP_200_OK)
        self.assertEqual(response.data['Success'], True)
        self.assertEqual(response.data['Message'],"Successful")

    def test_get_country_performance_post(self):
        view = winnersViewset.as_view({'post':'get_country_performance'})
        request = self.factory.post('country-performance/')
        response = view(request)
        self.assertEqual(response.data["Status"], status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data['Success'], False)