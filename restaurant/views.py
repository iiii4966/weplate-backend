from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import Restaurant, RestaurantImage, Menu, Food, FoodType
import json
import random

class MainRestaurantView(View):
    
    def get(self, request):
        random_int = random.randint(1, Restaurant.objects.count()-9)
        main_restaurant = RestaurantImage.objects.values('restaurant__id','restaurant__name','image').distinct()[random_int:random_int+9]        
        
        return JsonResponse({
                'main_restaurant' : list(main_restaurant)
                })

class DetailRestaurantView(View):
    
    def get(self, request):
        query_data = request.GET.get('data', '')

        try: 
            query_data = int(query_data) 
        except ValueError as err:
            query_data = query_data

        if type(query_data) == int:
            restaurant_id = query_data

            try:   
                restaurant = Restaurant.objects.select_related('food_type')
                select_restaurant = restaurant.values().get(id = restaurant_id)
                food_type = restaurant.values('food_type__name').get(id = restaurant_id)
                select_restaurant['food_type'] = food_type['food_type__name']
                menu = [menu for menu in Menu.objects.values('id','menu_name','price','image','food_id','food__name').filter(restaurant = restaurant_id)] 
            except ObjectDoesNotExist as err:
                return JsonResponse({"message":"NOT_FOUND"}, status = 404)
         
        elif type(query_data) == str and query_data != '':
            restaurant_name = query_data
            
            try:
                restaurant = Restaurant.objects.select_related('food_type')
                select_restaurant = restaurant.values().filter(name__icontains = restaurant_name)[0]
                food_type = restaurant.values('food_type__name').filter(name__icontains = restaurant_name)[0]
                select_restaurant['food_type'] = food_type['food_type__name']
                menu = [menu for menu in Menu.objects.values('id','price','image','food_id','food__name').filter(restaurant__name__icontains = restaurant_name)][:1]
            except ObjectDoesNotExist as err:
                return JsonResponse({"message":"NOT_FOUND"}, status = 404)
            except IndexError as err:
                return JsonResponse({"message":"NOT_FOUND"}, status = 404)
        else:
            return JsonResponse({"message":"NOT_FOUND"}, status = 404)
        
        return JsonResponse({
                'restarant_info': select_restaurant,
                'restaurant_menu': menu
                })
        
class NearbyRecommandRestaurantView(View):
    
    def get(self, request, recommand_id):
        try:
            restaurant_address = Restaurant.objects.get(pk = recommand_id).address 
            gu_data = restaurant_address.split()[1]
            nearby_restaurant = Menu.objects.filter(restaurant__address__icontains = gu_data)
            data = nearby_restaurant.values(
                    'id', 
                    'image', 
                    'restaurant__name',
                    'restaurant__price_range',
                    'restaurant__address',
                    'food__food_type__name',
                    )[:5]
            return JsonResponse(list(data), safe = False)
        except ObjectDoesNotExist as err:
            return JsonResponse({'message':'NOT_FOUND'}, status = 404)

class SearchRestaurantListView(View):

    def get(self, request):
        search_data = request.GET.get('search', '')
        
        if search_data == '':
            return JsonResponse({'message':'NOT_FOUND'}, status = 404)
        
        if search_data == '선릉':
                search_data = '역삼'

        try:
            data = list(Restaurant.objects.filter(Q(address__icontains = search_data) | Q(name__icontains = search_data)).values('id', 'name')[:6])
            return JsonResponse(data, safe = False)
        except Restaurant.DoesNotExist as err:
            return JsonResponse({"NOT_FOUND"}, status = 404)




                
