from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),  # handle all urls related to main application
    path('api/', include('base.api.urls'))  # handle all urls related to api
]
