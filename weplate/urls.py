from django.urls import path, include

urlpatterns = [
    path('', include('comments.urls')),
    path('', include('user.urls'))
   ]
