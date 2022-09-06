from django.urls import path, include
from . import views
from django.contrib.auth import views as authviews

app_name = "accounts"

urlpatterns = [
    path("register/", views.Register, name="signup view"),
    path("register/", views.RegisterAgent, name="agent signup view"),
    path("login/", views.Login, name="login view"),
    path("login/", views.LoginAgent, name="agent login view"),
    path("logout/", views.Logout, name="logout view"),
    path('user-profile/<str:first_name>/', views.UserProfile.as_view(), name="profile"),
    path('update-profile/', views.UpdateUserView.as_view(), name='update_profile'),
    path('change_password/', views.PasswordChangeView.as_view(template_name='user/changepassword'), name="change password"),
    path("delete-account/<int:pk>/", views.DeleteAccount.as_view(), name="delete account"),
    path('api/password_reset/', include('django_rest_passwordreset.urls'))
]
