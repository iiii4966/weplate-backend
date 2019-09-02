from django.db import models

# Create your models here.

class FoodType(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = "food_type"

class Restaurant(models.Model):
    name        = models.CharField(max_length = 30)
    food_type   = models.ForeignKey(FoodType, on_delete = models.SET_NULL, null=True)
    menu        = models.ManyToManyField('Food', through = 'Menu')
    address     = models.CharField(max_length = 50, null = True)
    phone       = models.CharField(max_length = 20, null = True)
    price_range = models.CharField(max_length = 20, null = True)
    parking     = models.CharField(max_length = 20, null = True)
    opening     = models.TimeField(auto_now = False, null = True)
    closing     = models.TimeField(auto_now = False, null = True)
    off_days    = models.CharField(max_length = 20, null = True)
    latitude    = models.DecimalField(max_digits = 20, decimal_places = 10, null = True)
    longitude   = models.DecimalField(max_digits = 20, decimal_places = 10, null = True)
    ratings     = models.IntegerField()
    deleted     = models.BooleanField(default = False, null = True)
    
    class Meta:
        db_table = "restaurant"

class RestaurantImage(models.Model):
    image      = models.URLField(max_length = 2500, null = True)
    restaurant = models.ForeignKey(Restaurant, on_delete = models.SET_NULL, null = True)
    
    class Meta:
        db_table = "restaurant_image"

class Food(models.Model):
    name      = models.CharField(max_length = 20)
    food_type = models.ForeignKey(FoodType, on_delete = models.SET_NULL, null = True)
   
    class Meta:
        db_table = "food"

class Menu(models.Model):
    food       = models.ForeignKey(Food, on_delete = models.SET_NULL, null = True)
    restaurant = models.ForeignKey(Restaurant, on_delete = models.SET_NULL, null = True, related_name = 'restaurant_set')
    name       = models.CharField(max_length = 50, null = True)
    price      = models.DecimalField(max_digits = 10, decimal_places = 3, null = True)
    image      = models.URLField(max_length = 2500, null = True)

    class Meta:
        db_table = "menu"
    

