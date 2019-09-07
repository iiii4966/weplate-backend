from django.urls import path
from .views import *

urlpatterns = [
    path('main_list', MainRestaurantView.as_view()),
    path('restaurant/<int:restaurant_id>', DetailRestaurantView.as_view()),
    path('near/<int:recommand_id>', NearbyRecommandRestaurantView.as_view()),
    path('map/<int:restaurant_id>', RestaurantMapView.as_view()),
    path('search', SearchRestaurantView.as_view())
   ]
