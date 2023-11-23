from django.shortcuts import render, redirect
from accueil.models import Projet
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required


def accueil(request):
    return render(request,'index.html')


@login_required(login_url=settings.LOGIN_URI)
def entreesystemes(request):
    NTPMB = False
    GRCMB = False
    droits = Projet.objects.filter(user_id=request.user.id)
    for droit in droits:
        if droit.projet == Projet.NTPMB:
            NTPMB = True
        elif droit.projet == Projet.GRCMB:
            GRCMB = True
        elif droit.projet == Projet.ALL:
            NTPMB = True
            GRCMB = True

    return render(request, "entreesystemes.html",
                      {
                        'NTPMB': NTPMB,
                        'GRCMB': GRCMB,
                      })
