from django.urls import path, include
from .views import winnerssViewset

urlpatterns = [
    path('marathons-summary/', winnerssViewset.as_view({"get":"get_marathons_summary"}), 
         name='marathons_summary'),
    path('races-summary/', winnerssViewset.as_view({"get":"get_races_summary"}), 
        name='races_summary'),
]
