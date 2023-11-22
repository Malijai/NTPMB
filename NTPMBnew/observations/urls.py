from django.urls import path
from .views import select_personne, creerdossier, saveMB, resumedossier, questions_pdf
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('', select_personne, name='SelectPersonne'),
    path('new/', creerdossier, name='creerdossier'),
    path('saveMB/<int:pid>/<int:qid>/<int:vid>/<int:auid>/', saveMB, name='saveMB'),
    path('voirMB/<int:pid>/', resumedossier, name='resumedossier'),
    path('FaitPDF/<int:qid>/', questions_pdf, name='questions_pdf'),
]
