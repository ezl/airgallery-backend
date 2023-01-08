from django.contrib import admin
from django.urls import path, include

from .drf_urls import urlpatterns as drf_urlpatterns


urlpatterns = [
    path('/', include("base.urls")),
    path('api/drf/', include(drf_urlpatterns)),
    path('api/', include("api.urls")),
    path('admin/', admin.site.urls),
]
