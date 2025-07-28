from django.urls import path
from .import views

urlpatterns = [
    path ('',views.index_view,name='index'),
    path('detail/<int:estate_pk>/',views.estate_detail_view,name='detail'),
    path('estate_like/<int:estate_id>/',views.user_estate_like_view,name='estate_like'),
    path('favorites/', views.favorite_estates_view, name='favorites'),
    
]
