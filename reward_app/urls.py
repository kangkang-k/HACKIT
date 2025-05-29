from django.urls import path
from reward_app import views

urlpatterns = [
    path('create_category/', views.CreateCategoryAPIView.as_view(), name='create_category'),
    path('update_category/<int:category_id>/', views.UpdateCategoryAPIView.as_view(), name='update_category'),
    path('list_categories/', views.ListCategoriesAPIView.as_view(), name='list_categories'),
    path('delete_category/<int:category_id>/', views.DeleteCategoryAPIView.as_view(), name='delete_category'),
    path('create_reward/', views.CreateRewardAPIView.as_view(), name='create_reward'),
    path('delete_reward/<int:reward_id>/', views.DeleteRewardAPIView.as_view(), name='delete_reward'),
    path('update_reward/<int:reward_id>/', views.UpdateRewardAPIView.as_view(), name='update_reward'),
    path('list_rewards/', views.ListRewardsAPIView.as_view(), name='list_rewards'),
    path('application_reward/', views.RewardApplicationCreateAPIView.as_view(), name='application_reward'),
    path('application_delete/<int:application_id>/', views.RewardApplicationDeleteAPIView.as_view(),
         name='application_delete'),
    path('application_accept/<int:application_id>/', views.RewardApplicationAcceptAPIView.as_view(),
         name='application_accept'),
    path('application_reject/<int:application_id>/', views.RewardApplicationRejectAPIView.as_view(),
         name='application_reject'),

]
