from django.db import models

# Create your models here.

class User(models.Model):
    user_id = models.CharField(max_length = 50, unique = True)
    password = models.CharField(max_length = 200)

    class Meta:
        db_table = 'Account'

