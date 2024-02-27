from django.shortcuts import render, redirect
import datetime
from datetime import date
# Create your views here.
# import logging
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from observations.models import MBpersonnes, Questionnaire, Questionnmb, MBresultats,Audience, Verdict
from grc.models import Personnegrc
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
import csv
from django.template import loader


DATE = datetime.datetime.now().strftime('%Y %b %d')

@login_required(login_url=settings.LOGIN_URI)
def select_personne(request):
    # Pour selectionner personne, questionnaire en fonction de l'assistant
    personnes = MBpersonnes.objects.filter(~Q(completed=1) & Q(assistant=request.user))
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
                    elif questionnaire.id == 21 and MBresultats.objects.filter(personne_id=pid, question__id=535,
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
                    auid = request.POST.get('hearing21')
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
                    reponse = date(int(an), int(mois), int(jour))
                    reponseaquestion = reponse
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
                                assistant_id=request.user.id,
                                )
        Personnegrc.objects.create(
                                codeGRC_id=Newid,
                                prenom=reponses['prenom'],
                                codeMB=reponses['personne_code'],
                                ferme=0,
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


# Pour l'exportation en streaming du CSV
class Echo(object):
    # An object that implements just the write method of the file-like interface.
    def write(self, value):
        # Write the value by returning it, instead of storing in a buffer
        return value


@login_required(login_url=settings.LOGIN_URI)
def prepare_csv(request, questionnaire, iteration, seuil):
    questions = Questionnmb.objects.\
                        filter(questionnaire_id=questionnaire).\
                        exclude(Q(typequestion_id=7) | Q(typequestion_id=100)).\
                        order_by('questionno').values('id', 'varname')
    inf = iteration * seuil
    sup = (iteration + 1) * seuil
    personnes = MBpersonnes.objects.all().values('id', 'code', 'completed', 'prenom', 'filecode')[inf:sup]

    toutesleslignes = fait_csv(questionnaire, personnes, questions, iteration)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exportation.txt"'

    now = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = 'Datas_{}_{}_L{}.csv'.format(questionnaire, now, iteration)
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
    response = StreamingHttpResponse((writer.writerow(row) for row in toutesleslignes),
                                     content_type="text/csv")
    response['Content-Disposition'] = 'attachment;  filename="' + filename + '"'
    return response


def fait_csv(questionnaire, personnes, questions, iteration):
    toutesleslignes = []
    entete = ['ID', 'code', 'Assistant', 'Verdict', 'Hearing']
    if questionnaire == 4:
        entete.append('Filecode')
        entete.append('Completed')
    for question in questions:
        entete.append(question['varname'])
    toutesleslignes.append(entete)
    for personne in personnes:
        assistants = MBresultats.objects.filter(personne_id=personne['id']).values_list('assistant_id', flat=True).distinct()
        for assistant in assistants:
            if questionnaire == 4:
                ligne = [personne['id'], personne['code'],  assistant, 'NA','NA', personne['filecode'], personne['completed']]
                for question in questions:
                    truc = faitdonnee(personne['id'], question['id'], assistant, 100, 100)
                    ligne.append(truc)
                toutesleslignes.append(ligne)
            else:
                verdicts = MBresultats.objects.order_by().filter(personne_id=personne['id'], assistant_id=assistant).\
                                                            exclude(verdict_id=100).\
                                                            values_list('verdict_id', flat=True).distinct()
                for verdict in verdicts:
                    if questionnaire == 10 or questionnaire == 11:
                        audiences =[100]
                    else:
                        audiences = MBresultats.objects.order_by().filter(personne_id=personne['id'],
                                                                        assistant_id=assistant, verdict_id=verdict).\
                                                                        exclude(audience_id=100).\
                                                                        values_list('audience_id', flat=True).distinct()
                    for audience in audiences:
                        ligne = [personne['id'], personne['code'], assistant, verdict, audience]
                        for question in questions:
                            truc = faitdonnee(personne['id'], question['id'], assistant, verdict, audience)
                            ligne.append(truc)
                        toutesleslignes.append(ligne)
    return toutesleslignes


@login_required(login_url=settings.LOGIN_URI)
def prepare_export(request):
    questionnaires = Questionnaire.objects.filter(Q(id__lte=30))
    if 'ExporterS' in request.POST:
        questionnaire = request.POST.get('questionnaireid')
        seuil = request.POST.get('seuil')
        return redirect('prepare_csv1', questionnaire=questionnaire, seuil=seuil)
    elif 'fait_entete_SPSS' in request.POST:
        questionnaire = request.POST.get('questionnaireid')
        return redirect('fait_entete_spss', questionnaire=questionnaire)
    return render(
        request,
        'choixexportations.html',
        {
            'questionnaires': questionnaires,
        }
    )

@login_required(login_url=settings.LOGIN_URI)
def prepare_csv1(request, questionnaire, seuil):
    nombre_personnes = MBpersonnes.objects.filter(Q(completed=1) | Q(completed=2)).count()
    questionnaire_nom = Questionnaire.objects.get(pk=questionnaire)
    #seuil = 150
    if nombre_personnes > seuil:
        reste = 0
        if nombre_personnes % seuil > 0:
            reste = 1
        iterations = int(nombre_personnes / seuil) + reste
    else:
        iterations = 1
    return render(request, 'page_extraction.html',
                  {
                      'iterations': range(iterations),
                      'questionnaire': questionnaire,
                      'questionnaire_nom': questionnaire_nom.nom_en,
                      'seuil': seuil,
                  })


def faitdonnee(personne, question, assistant, verdict, audience):
    truc = ""
    try:
        donnee = MBresultats.objects.filter(personne_id=personne, question_id=question,
                                            assistant_id=assistant,
                                            verdict_id=verdict,
                                            audience_id=audience).values('reponse_texte')
    except MBresultats.DoesNotExist:
        donnee = None
    if donnee:
        truc = donnee[0]['reponse_texte']
    else:
        truc = '-'
    return truc


@login_required(login_url=settings.LOGIN_URI)
def fait_entete_spss(request, questionnaire):
    ## Prepare les syntaxes pour exportation / importation des donnees pour les stats
    # Pour les syntaxes SPSS, fait le fichier des variables et des listes de valeurs
    response = HttpResponse(content_type='text/csv')
    filename1 = '"enteteSPSS_{}.sps"'.format(questionnaire)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename1)
    questions = Questionnmb.objects.filter(questionnaire_id=questionnaire). \
                                    exclude(Q(typequestion=7) | Q(typequestion=100)). \
                                    order_by('questionno')

    if questionnaire == 4:
        SD = 1
    else:
        SD = 0
    t = loader.get_template('spss_syntaxe.txt')
    response.write(
        t.render({'questions': questions, 'SD': SD}))
    return response

