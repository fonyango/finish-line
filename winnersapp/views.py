import pandas as pd
from rest_framework.response import Response
from rest_framework import viewsets, status
from .profiles import get_athletes_summary


# load data
df = pd.read_csv('datasets/marathons.csv')

class winnerssViewset(viewsets.ViewSet):

    def get_marathons_summary(self, request):
        """
        returns the summary of winners in all races
        """
        try:
            if request.method=='GET':

                winners_summary = get_athletes_summary(df)

            return Response({
                                "Success": True, 
                                "Status": status.HTTP_200_OK, 
                                "Message": "Successful", 
                                "Payload": winners_summary
                                })

        except Exception as e:
            print(e)
            return Response({
                                "Success": False, 
                                "Status": status.HTTP_501_NOT_IMPLEMENTED, \
                                "Message":"An error was encountered during execution"
                            })
