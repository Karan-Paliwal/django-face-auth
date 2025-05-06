from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('oppp.urls')),
    path('api/', include(('api.urls', 'api'), namespace='api')),  # Corrected namespace syntax
]