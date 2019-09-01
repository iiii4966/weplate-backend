from django.views import View
from django.http import JsonResponse
from .models import Restaurant, RestaurantImage, Menu, Food, FoodType
import json

# Create your views here.

class MainRestaurantView(View):
    
    def get(self, request):
        main_list = Restaurant.objects.values('id', 'name').distinct()[:6]
        image     = RestaurantImage.objects.values('image', 'restaurant_id').distinct().order_by('restaurant_id')[:6]
        
        return JsonResponse({
                'main_restaurant_name' : list(main_list),
                'restaurant_image' : list(image)
                })

class DetailRestaurantView(View):

    def get(self, request, *args, **kwargs):
        try:
            restaurant_id     = kwargs['restaurant_id']
            select_restaurant = Restaurant.objects.get(pk = restaurant_id)
            info      = Restaurant.objects.values().get(pk = restaurant_id)
            food_type = select_restaurant.food_type.name
            menu      = [menu for menu in Menu.objects.values().filter(restaurant = restaurant_id)]
        except KeyError as err:
            JsonResponse({"message":"NOT_FOUND"}, status = 404)
        except Restaurant.DoesNotExist as err:
            JsonResponse({"message":"NONE_INFO"}, status = 401)
               
        return JsonResponse({
                'restarant_info':info,
                'restaurant_food_type':food_type,
                'restaurant_menu':menu
                })
