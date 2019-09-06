from django.urls import path
from .views import *

urlpatterns = [
    path('main_list', MainRestaurantView.as_view()),
    path('restaurant', DetailRestaurantView.as_view()),
    path('restaurant/<int:recommand_id>', NearbyRecommandRestaurantView.as_view()),
    path('map/<int:restaurant_id>', RestaurantMapView.as_view()),
    path('search', SearchRestaurantListView.as_view())
   ]
