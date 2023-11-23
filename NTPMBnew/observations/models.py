from django.db import models
from django.contrib.auth.models import User

DEFAULT_UID = 1
# met tous les utilisateurs par defaut a 1 (maliadmin)

# Create your models here.
class MBpersonnes(models.Model):
    code = models.CharField(max_length=200, )
    completed = models.CharField(max_length=200, blank=True, null=True)
    dob = models.DateTimeField(blank=True, null=True)
    sdsexe = models.IntegerField(blank=True, null=True)
    filecode = models.CharField(max_length=200, blank=True, null=True)
    prenom = models.CharField(max_length=200, blank=True, null=True)
    assistant = models.ForeignKey(User, default=DEFAULT_UID, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grccompleted = models.CharField(max_length=200, blank=True, null=True)
    deathdate = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return '%s' % self.code


## Definit la forme html des questions ainsi que le type de réponse attendu (texte, bool, date etc)
class Typequestion(models.Model):
    nom = models.CharField(max_length=200, )
    latable = models.CharField(max_length=200, blank=True, null=True)
    taille = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom


##   listes valeurs non dependantes des provinces SANS province
class Listevaleur(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['typequestion', 'reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_en

class Victime(models.Model):
    #  listes de valeurs typequestion_id=14 (VICTIME)
    #  Restee a part a cause de la logique du tri des items
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s' % self.reponse_en


class Etablissement(models.Model):
    #   listes de valeurs typequestion_id=9 (ETABLISSEMENT)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_en']

    def __str__(self):
        return '%s' % self.reponse_en


class Municipalite(models.Model):
    #   listes de valeurs typequestion_id=15 (MUNICIPALITE)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_en']

    def __str__(self):
        return '%s' % self.reponse_en


class Questionnaire(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )
    description = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom_en


## Questions utilisees pour tous les questionnaires
# Parent_ID permet de lier l'affichage conditionnel d'une question en fonction de la réponse précédente
# à la question dont l'ID=Parent_id via la relation établie par  le champ relation et la valeur cible prédéfinie
# (par exemple question 2 s'ouvrira si question 1 (parent_id) a comme réponse 998 (cible) avec relation égale)
DEFAULT_PARENT_ID = 1

class Questionnmb(models.Model):
    questionno = models.IntegerField()
    questionen = models.CharField(max_length=255,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)
    typequestion = models.ForeignKey(Typequestion, on_delete=models.DO_NOTHING)
    parent = models.ForeignKey("self", default=DEFAULT_PARENT_ID, on_delete=models.DO_NOTHING)
    relation = models.CharField(blank=True, null=True, max_length=45,)
    cible = models.CharField(blank=True, null=True, max_length=45,)
    varname = models.CharField(blank=True, null=True, max_length=45,)
    aidefr = models.TextField(blank=True, null=True)
    aideen = models.TextField(blank=True, null=True)
    qstyle = models.CharField(blank=True, null=True, max_length=45,)
    parentvarname = models.CharField(blank=True, null=True, max_length=45,)

    class Meta:
        ordering = ['questionno']

    def __str__(self):
        return '%s' % self.questionen


## listes de valeurs des questions de typequestion_id=4 (CATEGORIAL)
# Pour les questions qui aparaissent rarement et dont les réponses sont des listes de valeur
class Reponsemb(models.Model):
    question = models.ForeignKey(Questionnmb, on_delete=models.DO_NOTHING)
    reponse_no = models.CharField(max_length=200)
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200,)
    reponse_fr = models.CharField(max_length=200,)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_en


class Audience(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )
    description = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom_en


class Verdict(models.Model):
    nom_en = models.CharField(max_length=200, )
    nom_fr = models.CharField(max_length=200, )
    description = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.nom_en


class MBresultats(models.Model):
    personne = models.ForeignKey(MBpersonnes, on_delete=models.DO_NOTHING)
    reponse_texte = models.CharField(max_length=255,)
    question = models.ForeignKey(Questionnmb, on_delete=models.DO_NOTHING)
    verdict = models.ForeignKey(Verdict, on_delete=models.DO_NOTHING)
    audience = models.ForeignKey(Audience, on_delete=models.DO_NOTHING)
    assistant = models.ForeignKey(User, default=DEFAULT_UID, on_delete=models.DO_NOTHING)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['personne', 'question', 'verdict', 'audience', 'assistant'], name='reponse_unique')
        ]

        def __str__(self):
            return '%s' % self.reponse_texte
