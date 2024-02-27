from django import template
from django.apps import apps
from observations.models import MBresultats, Reponsemb, Victime, Typequestion, Listevaleur
from django import forms
import re

register = template.Library()


#   pour les questions de Personne
@register.simple_tag
def creetextechar(qid, sorte, *args, **kwargs):
    name = "q" + str(qid)
    if sorte == 'STRING' or sorte == 'CODESTRING':
        question = forms.TextInput(attrs={'size': 30, 'id': name, })
    else:
        question = forms.NumberInput(attrs={'size': 30, 'id': name, })

    return question.render(name, '')


@register.simple_tag
def creedate(qid, *args, **kwargs):
    an = ''
    mois = ''
    jour = ''

    name = "q" + str(qid)
    day, month, year = fait_select_date(name, 1920, 2025)
    # name=q69_year, id=row...
    return year.render(name + '_year', an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


@register.simple_tag
def fait_select_date(idcondition, deb, fin):
    years = {x: x for x in range(deb, fin)}
    years[''] = ''
    years['99'] = 'UKN'
    days = {x: x for x in range(1, 32)}
    days[''] = ''
    days['99'] = 'UKN'

    months = (('', ''), (1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'),
              (9, 'Sept'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec'), ('99', 'UKN'))
    year = forms.Select(choices=years.items(), attrs={'id': idcondition})
    month = forms.Select(choices=months)
    day = forms.Select(choices=days.items())
    return day, month, year

@register.simple_tag
def creereponse(qid, *args, **kwargs):
    #   Pour listes de valeurs specifiques a chaque question
    defaultvalue = ''

    listevaleurs = Reponsemb.objects.filter(question_id=qid)
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')
    question = forms.Select(choices=liste, )
    #   return question.render(name, defaultvalue)
    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_reponse(qid, b, *args, **kwargs):
    #   Pour listes de valeurs specifiques a chaque question
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, vid=vid, auid=auid)
    idcondition = fait_id(qid, cible, relation=relation)

    listevaleurs = Reponsemb.objects.filter(question_id=qid)
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition})
    #   return question.render(name, defaultvalue)
    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_listes(qid, sorte, *args, **kwargs):
    #   Pour listes de valeurs specifiques a chaque question
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, vid=vid, auid=auid)
    idcondition = fait_id(qid, cible, relation=relation)
    sorteq = Typequestion.objects.get(nom=sorte)
    listevaleurs = Listevaleur.objects.filter(typequestion=sorteq)

    if sorte == "VIOLATION":
        liste = fait_liste_tables(listevaleurs, 'violation')
    else:
        liste = fait_liste_tables(listevaleurs, 'reponse')

    name = "q" + str(qid)

    question = forms.Select(choices=liste, attrs={'id': idcondition})
    #   return question.render(name, defaultvalue)
    return enlevelisttag(question.render(name, defaultvalue))


@register.simple_tag
def fait_date(qid, b, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']
    an = ''
    mois = ''
    jour = ''
    if MBresultats.objects.filter(personne__id=personneid, question__id=qid,
                                  assistant__id=assistant, verdict__id=vid, audience__id=auid).exists():
        ancienne = MBresultats.objects.get(personne__id=personneid, question__id=qid,
                                           assistant__id=assistant, verdict__id=vid, audience__id=auid)
        an, mois, jour = ancienne.reponse_texte.split('-')

    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    day, month, year = fait_select_date(idcondition, 1920, 2025)
#   name=q69_year, id=row...

    return year.render(name + '_year', an) + month.render(name + '_month', mois) + day.render(name + '_day', jour)


@register.simple_tag
def fait_textechar(qid, sorte, *args, **kwargs):
    #fait_textechar questid type persid=pid relation=relation cible=cible uid=user.id vid=vid auid=auid
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, vid=vid, auid=auid)
    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)

    if sorte == 'STRING' or sorte == 'TIME':
        question = forms.TextInput(attrs={'size': 30, 'id': idcondition})
    else:
        question = forms.NumberInput(attrs={'size': 30, 'id': idcondition})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_victimes(qid, *args, **kwargs):
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, vid=vid, auid=auid)
    idcondition = fait_id(qid, cible, relation=relation)

    listevaleurs = Victime.objects.all()
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_autres_tables(qid, sorte, *args, **kwargs):
    #   pour les tables dont la valeur a enregistrer n'est pas l'id mais la reponse_valeur
    #   et dont la liste depend de la province
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    sortetable = {"ETABLISSEMENT": "etablissement", "MUNICIPALITE": "municipalite"}
    tableext = sortetable[sorte]
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']

    defaultvalue = fait_default(personneid, qid, assistant=assistant, vid=vid, auid=auid)
    idcondition = fait_id(qid, cible, relation=relation)

    klass = apps.get_model('observations', tableext)
    #   klass = apps.get_model('dataentry', sortetable[b])
    listevaleurs = klass.objects.all()
    name = "q" + str(qid)
    liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition})

    return question.render(name, defaultvalue)


@register.simple_tag
def fait_table(qid, sorte, *args, **kwargs):
    #   questid sorte
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']
    sorte = sorte

    defaultvalue = fait_default(personneid, qid, assistant=assistant, vid=vid, auid=auid)
    idcondition = fait_id(qid, cible, relation=relation)

    sorteq = Typequestion.objects.get(nom=sorte)
    listevaleurs = Listevaleur.objects.filter(typequestion=sorteq)
    name = "q" + str(qid)
    if sorte == "VIOLATION":
        liste = fait_liste_tables(listevaleurs, 'violation')
    else:
        liste = fait_liste_tables(listevaleurs, 'reponse')

    question = forms.Select(choices=liste, attrs={'id': idcondition, 'name': name})
    return question.render(name, defaultvalue)


@register.simple_tag
def fait_ouinon(a, b, *args, **kwargs):
    qid = a
    sorte = b
    personneid = kwargs['persid']
    relation = kwargs['relation']
    cible = kwargs['cible']
    assistant = kwargs['uid']
    vid = kwargs['vid']
    auid = kwargs['auid']
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
    defaultvalue = fait_default(personneid, qid, assistant=assistant, vid=vid, auid=auid)
    idcondition = fait_id(qid, cible, relation=relation)
    name = "q" + str(qid)
    if sorte == "DICHO":
        liste = CHOIX_ON.items()
        question = forms.RadioSelect(choices=liste, attrs={'id': idcondition})
    else:
        liste = CHOIX_ONUK.items()
        question = forms.Select(choices=liste, attrs={'id': idcondition})

    return question.render(name, defaultvalue)


#   Utlitaires generaux
@register.filter
def fait_default(personneid, qid,  *args, **kwargs):
    #   fail la valeur par deffaut
    assistant = kwargs['assistant']
    vid = kwargs['vid']
    auid = kwargs['auid']
    ancienne = ''
    if MBresultats.objects.filter(personne__id=personneid, question__id=qid,
                                  assistant__id=assistant, verdict__id=vid, audience__id=auid).exists():
        reponse = MBresultats.objects.get(personne__id=personneid, question__id=qid,
                                           assistant__id=assistant, verdict__id=vid, audience__id=auid)
        ancienne=reponse.reponse_texte
    return ancienne


def fait_id(qid, cible, *args, **kwargs):
    #   fail l'ID pour javascripts ou autre
    relation = kwargs['relation']
    idcondition = "q" + str(qid)
    if relation != '' and cible != '':
        idcondition = 'row-{}X{}X{}'.format(qid, relation, cible)
    return idcondition


def fait_liste_tables(listevaleurs, sorte):
    liste = [('', '')]
    for valeur in listevaleurs:
        if sorte == 'reponse':
            val = valeur.reponse_valeur
            nen = valeur.reponse_en
            liste.append((val, nen))
        else:
            val = str(valeur.reponse_valeur)
            nen = val + ' - ' + valeur.reponse_en
            liste.append((val, nen))
    return liste


def enlevelisttag(texte):
    #   pour mettre les radiobutton sur une seule ligne
    texte = re.sub(r"(<ul[^>]*>)", r"", texte)
    texte = re.sub(r"(<li[^>]*>)", r"", texte)
    texte = re.sub(r"(</li>)", r"", texte)
    return re.sub(r"(</ul>)", r" ", texte)




