from django.urls import path, include
from .views import winnersViewset

urlpatterns = [
    path('profile/', winnersViewset.as_view({"post":"get_athletes_summary"}), 
         name='profile'),
    path('marathon/', winnersViewset.as_view({'post':"get_marathons_profile"}),
        name='marathon')
]
