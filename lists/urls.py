from django.urls import path
from lists import views

urlpatterns = [
    path('new', views.new_list, name='new_list'),
    path('<int:list_id>/', views.view_list, name='view_list'),
    path('<int:list_id>/add_movie', views.add_movie, name='add_movie'),
]