from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('about-me/', views.about, name = 'about'),
    path('delete/<list_id>', views.delete, name='delete'),
    path('completed/<list_id>', views.completed, name='completed'),
    path('not_completed/<list_id>', views.not_completed, name='not_completed'),
    path('edit/<list_id>', views.edit, name='edit')

]
