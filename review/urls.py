from django.urls import path
from .views import  FavoriteDeleteView, FavoriteListView



urlpatterns = [
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),
    path('favorites/<int:pk>/', FavoriteDeleteView.as_view(), name='delete'),
]
