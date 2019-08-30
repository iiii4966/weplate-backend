from django.db import models

# Create your models here.

class User(models.Model):

    user_id = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.user_id

    class Meta:
        db_table = 'Account'

