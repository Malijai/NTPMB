from django.urls import path
from .views import accueil, entreesystemes

urlpatterns = [
    path('', accueil, name='accueil'),
    path('datas', entreesystemes, name='entreesystemes'),
]
