from django.urls import path
from .views import *

urlpatterns = [
    path("/signup", UserSignUp.as_view()),
    path("/login", UserLogin.as_view()),
    path("/kakaologin", KakaoLoginView.as_view())
]
