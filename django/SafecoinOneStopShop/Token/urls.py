from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Wallet/', views.Wallet, name='Wallet'),
    path('WalletNew/', views.WalletNew, name='WalletNew'),
    path('NewToken/', views.NewToken, name='NewToken'),
    path('loadToken/', views.loadToken, name='loadToken'),
    path('NewTokenAcc/', views.NewTokenAcc, name='NewTokenAcc'),
    path('loadTokenAcc/', views.loadTokenAcc, name='loadTokenAcc'),
    path('ChangeChain/', views.ChangeChain, name='ChangeChain'),
    path('Balance/', views.Balance, name='Balance'),
    path('Airdrop/', views.airdrop, name='airdrop'),
    path('TKNBal/', views.TKNBal, name='TKNBal'),
    path('TKMint/', views.TKMint, name='TKMint'),
]
