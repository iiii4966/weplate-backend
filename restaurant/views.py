from django.views        import View
from django.http         import JsonResponse
from django.db.models    import Q
from .models             import Restaurant, RestaurantImage, Menu, Food, FoodType
from weplate.my_settings import KAKAO_AUTH_KEY

import json
import random
import requests

class MainRestaurantView(View):
    
    def get(self, request):
        random_int = random.randint(1, Restaurant.objects.count()-9)
        
        try:
            main_restaurant = RestaurantImage.objects.values('restaurant__id','restaurant__name','image').distinct()[random_int:random_int+9]        
            return JsonResponse(list(main_restaurant), safe = False)
        except RestaurantImage.DoesNotExist as err:
            return JsonRespone({"error":"NOT_FOUND"}, status = 404)

class DetailRestaurantView(View):
    
    def get(self, request, restaurant_id):
        try:
            restaurant_info = Restaurant.objects.values().get(id = restaurant_id)
            restaurant_info['menu'] = list(Menu.objects.filter(restaurant = restaurant_id).values())

            return JsonResponse({"restaurant_info":restaurant_info})
        except Restaurant.DoesNotExist as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
        except Menu.DoesNotExist as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
        
class NearbyRecommandRestaurantView(View):
    
    def get(self, request, recommand_id):
        try:
            restaurant_address = Restaurant.objects.get(pk = recommand_id).address 
            gu_data = restaurant_address.split()[1]
            data = Restaurant.objects.filter(address__icontains = gu_data).values(
                    'name',
                    'address',
                    'price_range', 
                    'food_type__name', 
                    'restaurantimage__image').distinct()[:5]
            return JsonResponse(list(data), safe = False)
        except Restaurant.DoesNotExist as err:
            return JsonResponse({'error':'NOT_FOUND'}, status = 404)
        except Menu.DoesNotExist as err:
            return JsonResponse({'error':'NOT_FOUND'}, status = 404)

class SearchRestaurantView(View):
    
     def get(self, request):
        restaurant = request.GET.get('data', '')
        
        if restaurant == '':
            return HttpResponse(status = 404)
        
        try:
            restaurant_info = Restaurant.objects.values().filter(Q(name__icontains = restaurant) | Q(address__icontains = restaurant))[0]
            restaurant_info['menu'] = list(Menu.objects.filter(restaurant = restaurant_info['id']).values())

            return JsonResponse({"restaurant_info":restaurant_info})
        except Restaurant.DoesNotExist as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
        except Menu.DoesNotExist as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
        except IndexError as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
 
class SearchRestaurantListView(View):

    def get(self, request):
        search_data = request.GET.get('data', '')
        
        if search_data == '':
            return JsonResponse({'error':'NOT_FOUND'}, status = 404)
        
        try:
            data = list(Restaurant.objects.filter(Q(address__icontains = search_data) | Q(name__icontains = search_data)).values('id', 'name')[:6])
            return JsonResponse(data, safe = False)
        except Restaurant.DoesNotExist as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)

class RestaurantMapView(View):
    
    def get(self, request, restaurant_id):
        url = "https://dapi.kakao.com/v2/local/geo/coord2address.json"
        header = {'Authorization' : KAKAO_AUTH_KEY}

        try:
            user_info = Restaurant.objects.get(id = restaurant_id)
            params = {
                    'x':user_info.longitude,
                    'y':user_info.latitude
                    }
            my_response = requests.get(url, headers=header, params = params, timeout=5).json()

            return JsonResponse(my_response)
        except Restaurant.DoesNotExist as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)
        except ConnetionError as err:
            return JsonResponse({"error":"NOT_FOUND"}, status = 404)

                
