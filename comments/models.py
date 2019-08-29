from django.db import models

# Create your models here.

class Comment(models.Model):
    user_id = models.CharField(max_length = 30)
    content = models.CharField(max_length = 500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    deleted_at = models.BooleanField(default = False)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']
