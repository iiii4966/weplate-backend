from django.urls import path, include
from django.conf import settings

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
        path('', include('comments.urls')),
        path('', include('user.urls')),
        path('', include('restaurant.urls'))
        ]
