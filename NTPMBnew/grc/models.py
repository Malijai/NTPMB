from django.db import models
from django.contrib.auth.models import User


## Code de violation
class Violation(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s %s' % (self.reponse_valeur, self.reponse_en)


## Tribunaux
class Tribunal(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_en

# Verdicts
class Verdict(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_en


class Type(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_en']

    def __str__(self):
        return '%s' % self.reponse_fr

class Duree(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_en

## Entrée des données
# Liste de tous les dossiers avec ou sans FPS
class Personnegrc(models.Model):
    codeGRC = models.ForeignKey('observations.MBpersonnes', on_delete=models.DO_NOTHING, primary_key=True)
    codeMB = models.CharField(max_length=200, verbose_name="Code MB")
    prenom = models.CharField(max_length=200, verbose_name="First name")
    dateprint = models.DateField(verbose_name='Date print: keep empty if no file', blank= True, null=True)
    newpresencefps = models.BooleanField(verbose_name="Check yes if there is a file or if it is indicated that it is not disclosable", blank=True, null=True)
    confidentiel = models.BooleanField(verbose_name="Is this file non disclosable? Check if yes", blank=True, null=True)
    ferme = models.BooleanField(blank=True, null=True)
    datedeces = models.DateField(verbose_name=" If there is a death date, enter it here", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)

    class Meta:
        ordering = ['codeMB']

    def __str__(self):
        return '%s' % self.codeMB


# Une fiche pour chaque délit de chaque personne.
class Delits(models.Model):
    personnegrc = models.ForeignKey(Personnegrc, on_delete=models.CASCADE, verbose_name="ID")
    date_sentence = models.DateField(verbose_name="Decision date")
    type_tribunal = models.ForeignKey(Tribunal, on_delete=models.DO_NOTHING, verbose_name="Tribunal type")
    lieu_sentence = models.ForeignKey('observations.Municipalite', on_delete=models.DO_NOTHING, verbose_name="Decision place")
    ordre_delit = models.IntegerField(default=1, verbose_name="Rank",)
    descriptiondelit = models.CharField(max_length=150, verbose_name="Offence description", null=True, blank=True)
    codeCCdelit = models.CharField(max_length=50, verbose_name="Offence CCCode number (if its not a CCC indicate which one. If no code type Unknown")
    nombre_chefs = models.IntegerField(default=1,verbose_name="Number of charges")
    violation = models.ForeignKey(Violation, on_delete=models.DO_NOTHING, verbose_name="Violation code")
    verdict = models.ForeignKey(Verdict, related_name='verdict', on_delete=models.DO_NOTHING, verbose_name="Verdict")
    amendeON = models.BooleanField(verbose_name="Fine, fees etc.? Check if yes")
    amende_type =  models.ForeignKey(Type, default=998, on_delete=models.DO_NOTHING, verbose_name="Fine caracteristics",null=True, blank=True)
    amendecout = models.IntegerField(default=0,verbose_name="Total cost of fine (+ surcharge + fees + restitution)", null=True, blank=True)
    detentionON = models.BooleanField(verbose_name="Custody? Check if yes")
    detentionduree = models.IntegerField(default=0, verbose_name="Custody length (add custody and pre-sentence custody)", null=True, blank=True)
    unitedetention =  models.ForeignKey(Duree, default=998, related_name='duree_detention', on_delete=models.DO_NOTHING, verbose_name="Days, months, years etc?", null=True, blank=True)
    probationON = models.BooleanField(verbose_name="Probation? Check if yes")
    probationduree = models.IntegerField(default=0, verbose_name="Probation length", null=True, blank=True)
    uniteprobation =  models.ForeignKey(Duree, default=998, related_name='duree_probation', on_delete=models.DO_NOTHING, verbose_name="Days, months, years etc?", null=True, blank=True)
    interdictionON = models.BooleanField(verbose_name="Ban/prohibition? Check if yes")
    interdictionduree = models.IntegerField(default=0, verbose_name="Prohibition length", null=True, blank=True)
    uniteinterdiction =  models.ForeignKey(Duree, default=998, related_name='duree_interdiction', on_delete=models.DO_NOTHING, verbose_name="Days, months, years etc?", null=True, blank=True)
    interdictiondetails = models.CharField(max_length=150, verbose_name="Details about prohibition", null=True, blank=True)
    surcisON = models.BooleanField(verbose_name="Suspended sentence? Check if yes")
    surcisduree = models.IntegerField(default=0, verbose_name="Suspension length", null=True, blank=True)
    unitesurcis =  models.ForeignKey(Duree, default=998, related_name='duree_surcis', on_delete=models.DO_NOTHING, verbose_name="Days, months, years etc?", null=True, blank=True)
    autreON = models.BooleanField(verbose_name="Other? Check if yes")
    autredetails = models.CharField(max_length=100, blank=True, null=True,verbose_name="If other: details")
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    card = models.IntegerField(default=1)
    nouveaudelit = models.BooleanField()

    class Meta:
        ordering = ['personnegrc', 'date_sentence', 'ordre_delit']
        unique_together = (('personnegrc', 'date_sentence', 'ordre_delit','RA'),)
        indexes = [models.Index(fields=['personnegrc', 'date_sentence', 'ordre_delit','RA'])]

    def __str__(self):
        return '%s %s %s' % (self.personnegrc, self.date_sentence, self.ordre_delit)


# Une fiche pour chaque liberation de chaque personne.
class Liberation(models.Model):
    personnegrc = models.ForeignKey(Personnegrc, on_delete=models.CASCADE, verbose_name="ID")
    date_liberation = models.DateField(verbose_name="Release date")
    type = models.BooleanField(verbose_name="Absolute dicharge? Check if yes")
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['personnegrc', 'date_liberation']

    def __str__(self):
        return '%s %s' % (self.personnegrc, self.date_liberation)