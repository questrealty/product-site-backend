from django.urls import path
from accounts.api import apiviews


app_name = "accounts"

urlpatterns = [
    path('register/', apiviews.RegisterView ,name='register'),
    path('register-agent', apiviews.RegisterAgentView, name='register agent'),
    path('login/', apiviews.LoginView ,name='login'),
    path('logout/', apiviews.LogoutView, name='logout'),

    path("user-details/<int:id>/", apiviews.user_details, name='user details'),
    path("user-update/<int:id>/", apiviews.user_update, name='user update'),
    path("user-delete/<int:id>/", apiviews.user_delete, name='user delete'),
    path("agent-details/", apiviews.agent_list, name='agent list')
]