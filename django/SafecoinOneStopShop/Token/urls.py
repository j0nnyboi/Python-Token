from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Home/', TemplateView.as_view(template_name='Home.html'),
         name='Home'),
    path('NFTs/', TemplateView.as_view(template_name='NFTs.html'),
         name='NFTs'),
    path('Token/', TemplateView.as_view(template_name='Token.html'),
         name='Token'),
    path('Wallet/', views.Wallet, name='Wallet'),
    path('WalletNew/', views.WalletNew, name='WalletNew'),
]
