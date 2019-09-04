from django.db import models


class SocialPlatforms(models.Model):
    platform = models.CharField(max_length=20)

    class Meta:
        db_table = "social_media_platform"


class UserAccount(models.Model):
    user_email = models.EmailField(max_length=100, unique=True)
    user_password = models.CharField(max_length=100)
    # SocialPlatforms이 삭제되더라도, 외래키 필드의 값이 null이 된다. 이때 null=True옵션이 반드시 필요
    social_platform = models.ForeignKey(
        SocialPlatforms, on_delete=models.SET_NULL, null=True, blank=True)
    social_login_id = models.CharField(max_length=50, null=True)
    user_fav_food = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.user_email + " " + self.user_password + " " + self.user_fav_food + self.user_kakao_id
