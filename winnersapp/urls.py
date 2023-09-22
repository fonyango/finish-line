from django.urls import path, include
from .views import winnerssViewset

urlpatterns = [
    path('profile/', winnerssViewset.as_view({"post":"get_athletes_summary"}), 
         name='profile'),
]
