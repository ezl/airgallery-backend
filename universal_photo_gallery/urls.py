from django.contrib import admin
from django.urls import path, include

from .drf_urls import urlpatterns as drf_urlpatterns


urlpatterns = [
    path('/', include("base.urls")),
    path('api/', include("api.urls")),
    path('drf/', include(drf_urlpatterns)),
    path('admin/', admin.site.urls),
]
