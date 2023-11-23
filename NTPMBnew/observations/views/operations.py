from django.shortcuts import render, redirect
import datetime
# Create your views here.
# import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from observations.models import MBpersonnes, Questionnaire, Questionnmb, MBresultats,Audience, Verdict
from grc.models import Personnegrc


@login_required(login_url=settings.LOGIN_URI)
def select_personne(request):
    # Pour selectionner personne, questionnaire en fonction de l'assistant
    personnes = MBpersonnes.objects.filter(~Q(completed=1)& Q(assistant=request.user))
    if request.method == 'POST':
        if request.POST.get('personneid') == '':
            messages.add_message(request, messages.ERROR, 'You have forgotten to chose a file')
            return render(
                request,
                'choix.html',
                    {
                    'personnes': personnes,
                    }
                )
        if 'Choisir' in request.POST:
            return redirect(
                            resumedossier,
                            request.POST.get('personneid'),
                            )
        elif 'Creer' in request.POST:
            return redirect(creerdossier)
    else:
        return render(
                    request,
                    'choix.html',
                    {
                        'personnes': personnes,
                        'message': 'welcome'
                    }
                )


@login_required(login_url=settings.LOGIN_URI)
def resumedossier(request, pid):
    Reponse = {
        '1': 'Started',
        '2': 'Finished',
    }
    vdts = Verdict.objects.all()
    hs = Audience.objects.all()
    nomcode = MBpersonnes.objects.get(id=pid).code
    reponsesauxquestionnaires = []
    if MBpersonnes.objects.filter(pk=pid, assistant=request.user).exists():
        questionnaires = Questionnaire.objects.filter(Q(id__lte=30))
        questionairelist = []
        for questionnaire in questionnaires:
            questionnaireitem = {}
            questionscible = Questionnmb.objects.get(Q(typequestion__id=1) & Q(questionnaire__id=questionnaire.id))
            questionnaireitem['questionscible']=questionscible
            questionnaireitem['qid']=questionnaire.id
#questionairelist.append(questionscible.questionen)
            questionnaireitem['reponses'] = []
            if MBresultats.objects.filter(personne_id=pid, question=questionscible, assistant=request.user).exists():
                resultats = MBresultats.objects.filter(personne_id=pid, question=questionscible, assistant=request.user)
                for resultat in resultats:
                    quest = {}
                    quest['verdict'] = resultat.verdict
                    quest['vid'] = resultat.verdict.id
                    quest['auid'] = resultat.audience.id
                    quest['audience'] = resultat.audience
                    quest['reponse_texte'] = Reponse[resultat.reponse_texte]
                    if questionnaire.id == 10 and  MBresultats.objects.filter(personne_id=pid, question__id=69, verdict=resultat.verdict,
                                                          audience=resultat.audience, assistant=request.user).exists():
                        date = MBresultats.objects.get(personne_id=pid, question__id=69, verdict=resultat.verdict,
                                                       audience=resultat.audience, assistant=request.user)
                        quest['date'] = date.reponse_texte
                    elif questionnaire.id == 11 and MBresultats.objects.filter(personne_id=pid, question__id=275,
                                                                                 verdict=resultat.verdict,
                                                                                 audience=resultat.audience,
                                                                                 assistant=request.user).exists():
                        date = MBresultats.objects.get(personne_id=pid, question__id=275, verdict=resultat.verdict,
                                                           audience=resultat.audience, assistant=request.user)
                        quest['date'] = date.reponse_texte
                    elif questionnaire.id == 20 and MBresultats.objects.filter(personne_id=pid, question__id=535,
                                                                               verdict=resultat.verdict,
                                                                               audience=resultat.audience,
                                                                               assistant=request.user).exists():
                        date = MBresultats.objects.get(personne_id=pid, question__id=535, verdict=resultat.verdict,
                                                       audience=resultat.audience, assistant=request.user)
                        quest['date'] = date.reponse_texte
                    else:
                        quest['date'] = 'NA'

                    questionnaireitem['reponses'].append(quest)
            else:
                #chercher dict defaults pour éviter ces 4 lignes
                questionnaireitem['reponses'].append({
                                            'verdict': '-',
                                            'audience':'-',
                                            'reponse_texte': 'Not started',
                                            'date': '-'
                                        })

            questionairelist.append(questionnaireitem)
        if request.method == 'POST':
            if 'Choisir10' in request.POST:
                if request.POST.get('verdict10') == '':
                    messages.add_message(request, messages.ERROR, 'You have forgotten to chose a verdict')
                    return render(
                        request,
                        'completedossier.html', {'donnees': questionairelist, 'pid': pid, 'code': nomcode,
                                                    'vdts': vdts, 'hs': hs}, )
                else:
                    vid=request.POST.get('verdict10')
                    return redirect(
                        saveMB,
                        pid,
                        10,
                        vid,
                        100
                    )
            elif 'Choisir11' in request.POST:
                if request.POST.get('verdict11') == '':
                    messages.add_message(request, messages.ERROR, 'You have forgotten to chose a verdict')
                    return render(
                        request,
                        'completedossier.html', {'donnees': questionairelist, 'pid': pid, 'code': nomcode,
                                                 'vdts': vdts, 'hs': hs}, )
                else:
                    vid = request.POST.get('verdict11')
                    return redirect(saveMB, pid, 11, vid, 100)
            elif 'Choisir21' in request.POST:
                if request.POST.get('verdict21') == '' or request.POST.get('hearing21') == '':
                    messages.add_message(request, messages.ERROR, 'You have forgotten to chose a verdict or a hearing')
                    return render(
                        request,
                        'completedossier.html', {'donnees': questionairelist, 'pid': pid, 'code': nomcode,
                                                 'vdts': vdts, 'hs': hs}, )
                else:
                    vid = request.POST.get('verdict21')
                    auid = request.POST.get('verdict21')
                    return redirect(
                        saveMB,
                        pid,
                        21,
                        vid,
                        auid
                    )
            elif 'Fermer' in request.POST:
                # pour fermer un dossier
                pid = request.POST.get('pid')
                personne = MBpersonnes.objects.get(pk=pid)
                if MBpersonnes.objects.filter(pk=pid, assistant=request.user).exists():
                    personne = MBpersonnes.objects.get(pk=pid, assistant=request.user)
                    personne.completed = 1
                    personne.save()
                    messages.add_message(request, messages.WARNING, personne.code + ' has been closed')
                else:
                    messages.add_message(request, messages.ERROR,
                                         personne.code + ' You are not allowed to close this file as you didn''t create it')
                personnes = MBpersonnes.objects.filter(~Q(completed=1) & Q(assistant=request.user))
                return render(
                    request,
                    'choix.html',
                    {
                        'personnes': personnes,
                    }
                )
    return render(request, 'completedossier.html', {'donnees': questionairelist, 'pid': pid, 'code': nomcode,
                                                    'vdts': vdts, 'hs': hs}, )



@login_required(login_url=settings.LOGIN_URI)
def creerdossier(request):
    qid = 500
    questionstoutes = Questionnmb.objects.filter(Q(questionnaire__id=qid) & Q(parentvarname=1))
    if request.method == 'POST':
        reponses = {}
        for question in questionstoutes:
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'TIME':
                an = request.POST.get('q{}_year'.format(question.id))
                if an != "":
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}-{}-{}".format(an, mois, jour)
                else:
                    reponseaquestion = ''
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if question.typequestion.nom == 'CODEDATE' or question.typequestion.nom == 'CODESTRING':
                    reponseaquestion = "encodee"
                    #reponseaquestion = encode_donnee(reponseaquestion)
                reponses[question.varname] = reponseaquestion
        pref = 50000
        dernier = MBpersonnes.objects.all().order_by('-id').first()
        reponses['personne_code'] = "{}_{}".format('MB', pref + dernier.id + 1,)
        Newid=dernier.id + 1
        MBpersonnes.objects.create(
                                id=Newid,
                                code=reponses['personne_code'],
                                filecode=reponses['Filecode'],
                                sdsexe=reponses['sdsexe'],
                                dob=reponses['dob'],
                                prenom=reponses['prenom'],
                                assistant_id=request.user.id
                                )
        Personnegrc.objects.create(
                                codeGRC_id=Newid,
                                prenom=reponses['prenom'],
                                codeMB=reponses['personne_code'],
                                ferme=0
                                )
        textefin=  "{}  has been created".format(reponses['personne_code'])
        messages.add_message(request, messages.ERROR, textefin)
        return redirect(resumedossier, Newid)
    else:
        return render(
                    request,
                    'creerdossier.html',
                    {'questions': questionstoutes}
                )


def faireautrechose(request):
    qid = 500
    questionstoutes = Questionnmb.objects.filter(questionnaire__id=qid)
    return render(
        request,
        'creerdossier.html',
        {'questions': questionstoutes}
        )


def faireunechose(request):
    qid = 500
    questionstoutes = Questionnmb.objects.filter(questionnaire__id=qid)
    return render(
        request,
        'creerdossier.html',
        {'questions': questionstoutes}
        )


@login_required(login_url=settings.LOGIN_URI)
def saveMB(request, pid, qid, vid, auid):
    # genere le questionnaire demande NON repetitif
    ascendancesF, ascendancesM, questionstoutes = genere_questions(qid)
    nomcode = MBpersonnes.objects.get(id=pid).code
    questionnaire = Questionnaire.objects.get(id=qid).nom_en
    verdict = Verdict.objects.get(id=vid)
    audience = Audience.objects.get(id=auid)

    if request.method == 'POST':
        for question in questionstoutes:
            if question.typequestion.nom == 'DATE' or question.typequestion.nom == 'CODEDATE' or \
                            question.typequestion.nom == 'DATEH' or question.typequestion.nom == 'TIME':
                reponseaquestion = ''
                an = request.POST.get('q{}_year'.format(question.id))
                if an:
                    mois = request.POST.get('q{}_month'.format(question.id))
                    jour = request.POST.get('q{}_day'.format(question.id))
                    reponseaquestion = "{}-{}-{}".format(an, mois, jour)
            else:
                reponseaquestion = request.POST.get('q' + str(question.id))
            if reponseaquestion:
                if not MBresultats.objects.filter(personne_id=pid, question=question, assistant=request.user, reponse_texte=reponseaquestion,verdict=vid, audience=auid).exists():
                    MBresultats.objects.update_or_create(personne_id=pid, question=question, assistant=request.user, verdict=verdict, audience=audience,
                                # update these fields, or create a new object with these values
                                defaults={
                                    'reponse_texte': reponseaquestion,
                                }
                            )
        now = datetime.datetime.now().strftime('%H:%M:%S')
        messages.add_message(request, messages.WARNING, 'Data saved at ' + now)

    return render(request,
                  'savenMB.html',
                  {
                      'qid': qid,
                      'pid': pid,
                      'vid': vid,
                      'auid': auid,
                      'questions': questionstoutes,
                      'ascendancesM': ascendancesM,
                      'ascendancesF': ascendancesF,
                      'code': nomcode,
                      'questionnaire': questionnaire,
                      'verdict': verdict,
                      'audience': audience,
                  }
                )


def genere_questions(qid):
    questionstoutes = Questionnmb.objects.filter(Q(questionnaire__id=qid) & Q(parentvarname=1))
    enfants = questionstoutes.select_related('typequestion', 'parent').filter(questionnmb__parent__id__gt=1)
    ascendancesM = {rquestion.id for rquestion in questionstoutes.select_related('typequestion').filter(Q(pk__in=enfants) & Q(parentvarname=1))}
    ascendancesF = set()  # liste sans doublons
    for rquestion in questionstoutes:
        for fille in questionstoutes.select_related('typequestion').filter(parent__id=rquestion.id):
            # #va chercher si a des filles (question_ fille)
            ascendancesF.add(fille.id)
    return ascendancesF, ascendancesM, questionstoutes




