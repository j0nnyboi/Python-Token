from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Token/', views.Token, name='Token'),
    path('images/SafeCoin_Icon.png', views.images, name='images'),
]
