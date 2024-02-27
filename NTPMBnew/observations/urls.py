from django.urls import path
from .views import select_personne, creerdossier, saveMB, resumedossier, questions_pdf, prepare_csv1, \
    prepare_csv, prepare_export, fait_entete_spss
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login', kwargs={'redirect_authenticated_user': True}),
    path('', select_personne, name='SelectPersonne'),
    path('new/', creerdossier, name='creerdossier'),
    path('saveMB/<int:pid>/<int:qid>/<int:vid>/<int:auid>/', saveMB, name='saveMB'),
    path('voirMB/<int:pid>/', resumedossier, name='resumedossier'),
    path('FaitPDF/<int:qid>/', questions_pdf, name='questions_pdf'),
    path('Faitcsv/<int:questionnaire>/<int:iteration>/<int:seuil>/', prepare_csv, name='prepare_csv'),
    path('Prepareexport/', prepare_export, name='prepare_export'),
    path('csv/<int:questionnaire>/<int:seuil>', prepare_csv1, name='prepare_csv1'),
    path('enteteSPSS_S/<int:questionnaire>/', fait_entete_spss, name='fait_entete_spss'),
]
