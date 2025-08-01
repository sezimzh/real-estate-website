from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.user_register_view,name='user_register'),
    path('login/',views.user_login_view,name='user_login'),
    path('logout/',views.user_logout_views,name='user_logout'),
    path('otp_verify/<int:user_id>/', views.user_otp_verify_view,name='otp_verify'),
    path('profile/', views.user_profile_view,name='profile'),
]