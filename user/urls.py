from django.urls import path
from .import views

urlpatterns = [
    path('register/',views.user_register_view,name='user_register'),
    path('login/',views.user_login_view,name='user_login'),
    path('logout/',views.user_logout_views,name='user_logout'),
]