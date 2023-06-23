import pandas as pd
from rest_framework.response import Response
from rest_framework import viewsets, status
from .profiles import Marathons


# load data
df = pd.read_csv('datasets/marathons.csv')
marathons = Marathons(df)



class winnerssViewset(viewsets.ViewSet):

    def get_marathons_summary(self, request):
        """
        returns the summary of winners in all races
        """
        try:
            if request.method=='GET':

                winners_summary = marathons.get_athletes_summary()

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
        
    
    def get_races_summary(self, request):
        """
        returns the summary of races in all marathons
        """
        # try:
        if request.method=='GET':

            result = marathons.get_marathons_summary()

        return Response({
                            "Success": True, 
                            "Status": status.HTTP_200_OK, 
                            "Message": "Successful", 
                            "Payload": result
                                })

        # except Exception as e:
        #     print(e)
        #     return Response({
        #                         "Success": False, 
        #                         "Status": status.HTTP_501_NOT_IMPLEMENTED, \
        #                         "Message":"An error was encountered during execution"
        #                     })

