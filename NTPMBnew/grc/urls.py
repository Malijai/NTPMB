from django.urls import path
from .views import liste_personne, personne_delits, personne_ferme, do_dico_pdf, personne_edit, supp_delit


urlpatterns = [
    path('personne/<int:pk>/edit/', personne_edit, name='personne_edit'),
    path('delits/<int:pk>/', personne_delits, name='personne_delits'),
    path('', liste_personne, name='liste_personne'),
    path('ferme/<int:pk>/',personne_ferme, name='personne_ferme'),
    path('do_pdf/', do_dico_pdf, name='do_dico_pdf'),
    path('enleve/<int:id>/', supp_delit, name='supp_delit'),
]