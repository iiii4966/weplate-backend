from django.db import models
from user.models import User
# Create your models here.

class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete = models.CASCADE)
    content    = models.CharField(max_length = 500, null = True, blank = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted    = models.BooleanField(default = False, null = True)

    class Meta:
        db_table = 'comments'


