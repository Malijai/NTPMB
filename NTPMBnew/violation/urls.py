from django.urls import path
from .views import rechercher
from django.views.generic import TemplateView


urlpatterns = [
    path('', rechercher, name='Rechercherviol'),
    path('listevcc.html', TemplateView.as_view(template_name="listevcc.html"), name='listevccs'),
]

