import pandas as pd
from rest_framework.response import Response
from rest_framework import viewsets, status
from .profiles import Marathons, DataExtractor
from helpers.utils import Starter


# instantiate Starter & DataExtractor class
starter = Starter()
db = starter.set_up_database()
data_extractor = DataExtractor(db)


class winnersViewset(viewsets.ViewSet):

    def get_athletes_summary(self, request):
        """
        returns the summary of winners in all races
        """
        try:
            if request.method=='POST':
                athlete_id = request.data['athlete_id']
                df = data_extractor.get_athletes_profile_data(athlete_id)
                
                # check if 'athleteid' not there ==> dataframe is empty
                if df.empty==True:

                    return Response({
                                "Success": False, 
                                "Status": status.HTTP_204_NO_CONTENT, 
                                "Message": "No Data Found", 
                                "Payload": None
                                })
                                
                # instantiate Marathon class
                marathons = Marathons(df)
                result = marathons.get_athletes_profile()

                return Response({
                                    "Success": True, 
                                    "Status": status.HTTP_200_OK, 
                                    "Message": "Successful", 
                                    "Payload": result
                                    })
            else:
                return Response({
                            "Success": False, 
                            "Status": status.HTTP_405_METHOD_NOT_ALLOWED, 
                            "Message": "Method Not Allowed", 
                            "Payload": None
                            })


        except Exception as e:
            print(e)
            return Response({
                                "Success": False, 
                                "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                                "Message":"An error was encountered during execution"
                            })
    
    def get_marathons_profile(self, request):
        """
        returns the summary of marathons
        """
        try:
            if request.method=='POST':
                marathon_id = request.data['marathon_id']
                df = data_extractor.get_marathon_profile_data(marathon_id)
                
                # check if 'marathonid' not there ==> dataframe is empty
                if df.empty==True:

                    return Response({
                                "Success": False, 
                                "Status": status.HTTP_204_NO_CONTENT, 
                                "Message": "No Data Found", 
                                "Payload": None
                                })
                                
                # instantiate Marathon class
                marathons = Marathons(df)
                result = marathons.get_marathons_summary()

                return Response({
                                    "Success": True, 
                                    "Status": status.HTTP_200_OK, 
                                    "Message": "Successful", 
                                    "Payload": result
                                    })

            else:
                return Response({
                            "Success": False, 
                            "Status": status.HTTP_405_METHOD_NOT_ALLOWED, 
                            "Message": "Method Not Allowed", 
                            "Payload": None
                            })

        except Exception as e:
            print(e)
            return Response({
                                "Success": False, 
                                "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                                "Message":"An error was encountered during execution"
                            })
    
    def get_country_performance(self, request):
        """
        returns the summary of country performance
        """
        try:
            if request.method=='GET':
               
                df = data_extractor.get_country_performance_data()
                
                # check if dataframe is empty
                if df.empty==True:

                    return Response({
                                    "Success": False, 
                                    "Status": status.HTTP_204_NO_CONTENT, 
                                    "Message": "No Data Found", 
                                    "Payload": None
                                    })
                                
                # instantiate Marathon class
                marathons = Marathons(df)
                result = marathons.get_country_summary()

                return Response({
                                    "Success": True, 
                                    "Status": status.HTTP_200_OK, 
                                    "Message": "Successful", 
                                    "Payload": result
                                    })

            else:
                return Response({
                                "Success": False, 
                                "Status": status.HTTP_405_METHOD_NOT_ALLOWED, 
                                "Message": "Method Not Allowed", 
                                "Payload": None
                                })

        except Exception as e:
            print(e)
            return Response({
                                "Success": False, 
                                "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                                "Message":"An error was encountered during execution"
                            })

    def get_race_time_trends(self, request):
        """
        returns timetaken for the race of the marathon
        """
        try:
            if request.method=='POST':
                raceID = request.data['raceID']
                marathonID = request.data['marathonID']

                df = data_extractor.get_athlete_best_times_data(raceID,marathonID)
                
                # check if dataframe is empty
                if df.empty==True:

                    return Response({
                                    "Success": False, 
                                    "Status": status.HTTP_204_NO_CONTENT, 
                                    "Message": "No Data Found", 
                                    "Payload": None
                                    })
                                
                # instantiate Marathon class
                marathons = Marathons(df)
                result = marathons.get_athlete_best_times()

                return Response({
                                    "Success": True, 
                                    "Status": status.HTTP_200_OK, 
                                    "Message": "Successful", 
                                    "Payload": result
                                    })

            else:
                return Response({
                                "Success": False, 
                                "Status": status.HTTP_405_METHOD_NOT_ALLOWED, 
                                "Message": "Method Not Allowed", 
                                "Payload": None
                                })

        except Exception as e:
            print(e)
            return Response({
                                "Success": False, 
                                "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                                "Message":"An error was encountered during execution"
                            })
