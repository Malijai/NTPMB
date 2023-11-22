# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from observations.models import Questionnaire, Questionnmb, Listevaleur, Reponsemb, Victime, Typequestion
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
#A necessite l'installation de reportlab (pip install reportlab)
import datetime

NOM_FICHIER_PDF = "MB_NTP1_P2.pdf"
TITRE = "Manitoba NTP1 replication part2"
PAGE_INFO = " Data protocol - Printed date: " + datetime.datetime.now().strftime('%Y/%m/%d')
PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]
styles = getSampleStyleSheet()
DATE = datetime.datetime.now().strftime('%Y %b %d')

#Exportation des questions en PDF
def myFirstPage(patron, _):
    patron.saveState()
    patron.setFont('Helvetica',16)
    patron.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT-108, TITRE)
    patron.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 130, DATE)
    patron.setFont('Helvetica',10)
    patron.setStrokeColorRGB(0, 0, 0)
    patron.setLineWidth(0.5)
    patron.line(0, 65, PAGE_WIDTH - 0, 65)
    patron.drawString(inch, 0.70 * inch, "NTP Community / %s" % PAGE_INFO)
    patron.restoreState()


def myLaterPages(patron, doc):
    patron.saveState()
    patron.setFont('Helvetica',10)
    patron.setStrokeColorRGB(0, 0, 0)
    patron.setLineWidth(0.5)
    patron.line(0, 65, PAGE_WIDTH - 0, 65)
    patron.drawString(inch, 0.70 * inch, "Page %d %s" % (doc.page, PAGE_INFO))
    patron.restoreState()


@login_required(login_url=settings.LOGIN_URI)
def questions_pdf(request, qid):
    fichier = 'QID_' + str(qid) + '_' + NOM_FICHIER_PDF
#    doc = SimpleDocTemplate("/tmp/{}".format(NOM_FICHIER_PDF))
    doc = SimpleDocTemplate("/tmp/{}".format(fichier))
    questionnaire=Questionnaire.objects.get(pk=qid)
    Story = [Spacer(1,1.5 * inch)]
    Story.append(Paragraph(questionnaire.nom_en, styles["Heading1"]))
    Story.append(Spacer(1, 0.5 * inch))
#    Story = [] # (si on ne veut pas de premiere page differente on ne met pas d'Espace en haut de la 1ere)
    style = styles['Code']
    bullettes = styles['Code']
#    articles_list = Article.objects.all()
#    for article in articles_list:
#    im = '<img src="media/images/pointblanc.jpg"/>'
    viol = 0
    for question in Questionnmb.objects.filter(questionnaire_id=qid):
        if question.typequestion.nom == 'TITLE':
            ptext = "<b>{}</b>".format(question.questionen)
            Story.append(Spacer(1, 0.2 * inch))
            Story.append(Paragraph(ptext, styles["Heading3"]))
            Story.append(Paragraph(".&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Question text", styles["Normal"]))
        elif question.typequestion.nom == 'COMMENT':
            ptext = "<b>{}</b>".format(question.questionen)
            Story.append(Paragraph(ptext, styles["Heading4"]))
            Story.append(Paragraph(".&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Variable Name &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Question text", styles["Normal"]))
        else:
            x = 15 - len(question.varname)
            espace = ''
            for i in range(0, x):
                espace = espace + '&nbsp;'
            bogustext = question.varname + espace + question.questionen
            p = Paragraph(bogustext, style)
            Story.append(p)
        if question.typequestion.nom == "DICHO":
            liste = [(1, 'Yes'), (0, 'No')]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
#                bogustext = '&#124;' + espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                bogustext = espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "DICHON" or question.typequestion.nom == "DICHOU":
            liste = [(1, 'Yes'), (0, 'No'), (98, 'NA'), (99, 'Unknown')]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "BOOLEAN":
            liste = [(1, 'Started'), (2, 'Finished')]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "COUR":
            liste = [(1, 'Municipal'), (2, 'Provincial'), (3, 'Superior'),]
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = '&#124;' + espace + str(list[0]) + '&nbsp;&nbsp;' + str(list[1])
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "CATEGORIAL":
            liste = Reponsemb.objects.filter(question_id=question.id )
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = espace + str(list.reponse_valeur) + '&nbsp;&nbsp;' + str(list.reponse_en)
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "HCR20" or question.typequestion.nom == "POSOLOGIE" :
            liste = Listevaleur.objects.filter(typequestion=question.typequestion.id)
            for list in liste:
                espace = '&nbsp;'*25 +'&#x00B7;'
                bogustext = espace + str(list.reponse_valeur) + '&nbsp;&nbsp;' + str(list.reponse_en)
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "VICTIME":
            liste = Victime.objects.all()
            for list in liste:
                espace = '&nbsp;' * 25 + '&#x00B7;'
                bogustext = espace + str(list.reponse_valeur) + '&nbsp;&nbsp;' + str(list.reponse_en)
                p = Paragraph(bogustext, bullettes)
                Story.append(p)
        elif question.typequestion.nom == "PAYS" or question.typequestion.nom == "LANGUE":
            bogustext = '&nbsp;' * 20 + "Stat can list of Countries or Languages"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)
        elif question.typequestion.nom == "VIOLATION":
            viol = 1
            bogustext = '&nbsp;' * 20 + "See VIOLATION CODES at the end of the document"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)
        elif question.typequestion.nom =="ETABLISSEMENT" or question.typequestion.nom == "MUNICIPALITE":
            bogustext = '&nbsp;' * 20 + "List of available Hospitals or Courts in Manitoba"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)
        elif question.typequestion.nom == "CODEDATE" or question.typequestion.nom == "CODESTRING":
            bogustext = '&nbsp;' * 20 + "Data will be encrypted before saving"
            p = Paragraph(bogustext, bullettes)
            Story.append(p)

    if viol == 1:
        ptext = "VIOLATION CODES"
        #Story.append(Spacer(1, 0.2 * inch))
        Story.append(PageBreak())
        Story.append(Paragraph(ptext, styles["Heading3"]))
        typeviol = Typequestion.objects.get(nom='VIOLATION')
        liste = Listevaleur.objects.filter(typequestion=typeviol.id)
        for list in liste:
            espace1 = '&nbsp;'*3 + '&#x00B7;'
            espace2 = '&nbsp;'*3
            bogustext = espace1 + str(list.id) + espace2 + list.reponse_en
            p = Paragraph(bogustext,  bullettes)
            Story.append(p)

    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)

    fs = FileSystemStorage("/tmp")
    with fs.open(fichier) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(fichier)
    return response