from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('zingsa/', include('zingsa_app.urls')),
    path('', include('zingsa_app.urls')), 
]
