from django.views import View
from django.http import JsonResponse
from .models import Restaurant, RestaurantImage, Menu, Food, FoodType
import json
import random 

# Create your views here.

class MainRestaurantView(View):
    
    def get(self, request):
        random_int = random.randint(1, Restaurant.objects.count()-10)
        main_list = Restaurant.objects.values('id', 'name').distinct()[random_int:random_int+10]
        image     = RestaurantImage.objects.values('image', 'restaurant_id').distinct().order_by('restaurant_id')[random_int:random_int+10]
        
        return JsonResponse({
                'main_restaurant_name' : list(main_list),
                'restaurant_image' : list(image)
                })

class DetailRestaurantView(View):

    def get(self, request, restaurant_id):
        try:   
            select_restaurant = Restaurant.objects.get(pk = restaurant_id)
            info      = Restaurant.objects.values().get(pk = restaurant_id)
            food_type = select_restaurant.food_type.name
            menu      = [menu for menu in Menu.objects.values().filter(restaurant = restaurant_id)]  
        except Restaurant.DoesNotExist as err:
            return JsonResponse({"message":"INVALID_REQUEST"}, status = 401) 
             
        return JsonResponse({
                'restarant_info':info,
                'restaurant_food_type':food_type,
                'restaurant_menu':menu
                })
