from django import template
from django.apps import apps
from observations.models import Reponsemb, Victime, Typequestion, Listevaleur
from accueil.models import User

register = template.Library()

@register.simple_tag
def spss_dichou(type, *args, **kwargs):
    CHOIX_ON = {
        1: 'Yes',
        0: 'No'
    }
    CHOIX_ONUK = {
        '': '',
        1: 'Yes',
        0: 'No',
        98: 'NA',
        99: 'Unknown'
    }
    if type == "DICHO":
        liste = CHOIX_ON.items()
    else:
        liste = CHOIX_ONUK.items()
    return fait_rendu(liste)


@register.simple_tag
def spss_table_valeurs(type, *args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur
    #et dont la liste depend de la province
    typetable = {"ETABLISSEMENT": "etablissement", "MUNICIPALITE": "municipalite",}
    tableext = typetable[type]

    Klass = apps.get_model('observations', tableext)
    # Klass = apps.get_model('dataentry', typetable[b])
    listevaleurs = Klass.objects.all()
    liste = spss_liste_tables(listevaleurs, 'reponse')
    return fait_rendu(liste)


@register.simple_tag
def spss_table_victime(*args, **kwargs):
    #pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur (independant de la province)
    listevaleurs = Victime.objects.all()
    liste = spss_liste_tables(listevaleurs, 'reponse')
    return fait_rendu(liste)


@register.simple_tag
def spss_reponse(qid, *args, **kwargs):
    #Pour listes de valeurs specifiques a chaque question
    listevaleurs = Reponsemb.objects.filter(question_id=qid, )
    liste = spss_liste_tables(listevaleurs, 'reponse')
    return fait_rendu(liste)


@register.simple_tag
def spss_liste_tables(listevaleurs, type):
    liste = []
    for valeur in listevaleurs:
        if type == 'reponse':
            val = valeur.reponse_valeur
            nen = valeur.reponse_en
            liste.append((val, nen))
        elif type == 'violation':
            val = str(valeur.reponse_valeur)
            nen = val + ' - ' + valeur.reponse_en
            liste.append((val, nen))
    return liste


@register.simple_tag
def spss_table(type, *args, **kwargs):
    #questid type
    typeq = Typequestion.objects.get(nom=type)
    listevaleurs = Listevaleur.objects.filter(typequestion=typeq)
    if type == "VIOLATION":
        liste = spss_liste_tables(listevaleurs, 'violation')
    else:
        liste = spss_liste_tables(listevaleurs, 'reponse')
    return fait_rendu(liste)


@register.simple_tag
def fait_rendu(liste):
    sortie = ''
    nb = len(liste)
    for i, val in enumerate(liste, 1):
        sortie += '{}        "{}"'. format(val[0], val[1])
        if i == nb:
            sortie += "/\n."
        else:
            sortie += "\n"
    return sortie


@register.simple_tag
def fait_ras():
    liste = User.objects.all()
    sortie = ''
    nb = len(liste)
    for i, user in enumerate(liste, 1):
        sortie += '{}        "{}"'. format(user.id, user.username)
        if i == nb:
            sortie += "/\n."
        else:
            sortie += "\n"
    return sortie
