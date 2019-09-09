from django.db import models
from user.models import User
from restaurant.models import Restaurant

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    Restaurant = models.ForeignKey(Restaurant, on_delete = models.SET_NULL, null = True)
    content    = models.CharField(max_length = 500, null = True, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted     = models.BooleanField(default = False, null = True)
   
    class Meta:
        db_table = 'comment'


