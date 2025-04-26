from django.urls import path

from bounty import views

urlpatterns = [
    path('create_bounty/', views.create_bounty, name='create_bounty'),
]
