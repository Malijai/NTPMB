from django.shortcuts import render, redirect
from violation.models import Codecriminel, Violation
from .form import ChercheForm
from django.db.models import Q


def rechercher(request):
    form_class = ChercheForm
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid():
            texte = request.POST.get('recherchetexte', '')
            codes = Codecriminel.objects.filter(Q(reponse_valeur__icontains=texte))
            if codes:
                return render(request, 'listevcc.html', {'codes': codes})
            else:
                return render(request, 'recherchecode.html', {'form': form_class, 'message': texte})
    else:
        form_class = ChercheForm()

    return render(request, 'recherchecode.html', {'form': form_class})