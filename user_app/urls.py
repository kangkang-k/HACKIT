from django.urls import path

from user_app import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('update/', views.UserUpdateView.as_view(), name='update'),
    path('update2/', views.UserUpdateView2.as_view(), name='update2'),
    path('change_password/', views.change_password, name='change_password'),
    path('balance_update/', views.BalanceUpdateView.as_view(), name='balance_update'),
]
