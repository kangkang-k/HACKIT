from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_app/',include('user_app.urls')),
    path('reward_app/',include('reward_app.urls')),
]
