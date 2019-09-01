from django.urls import path
from .views import *

urlpatterns = [
    path('main_list', MainRestaurantView.as_view()),
    path('main_list/<int:restaurant_id>', DetailRestaurantView.as_view())
   ]
