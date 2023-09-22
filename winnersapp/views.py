import pandas as pd
from rest_framework.response import Response
from rest_framework import viewsets, status
from .profiles import Marathons, get_athletes_profile_data

class winnerssViewset(viewsets.ViewSet):

    def get_athletes_summary(self, request):
        """
        returns the summary of winners in all races
        """
        try:
            if request.method=='POST':
                athlete_id = request.data['athlete_id']
                df = get_athletes_profile_data(athlete_id)
                
                if df.empty==True:

                    return Response({
                                "Success": True, 
                                "Status": status.HTTP_204_NO_CONTENT, 
                                "Message": "No data found", 
                                "Payload": None
                                })

                marathons = Marathons(df)
                result = marathons.get_athletes_profile()

            return Response({
                                "Success": True, 
                                "Status": status.HTTP_200_OK, 
                                "Message": "Successful", 
                                "Payload": result
                                })

        except Exception as e:
            print(e)
            return Response({
                                "Success": False, 
                                "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                                "Message":"An error was encountered during execution"
                            })
    

