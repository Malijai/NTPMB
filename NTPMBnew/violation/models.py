from django.db import models
# Create your models here.


class Violation(models.Model):
    reponse_valeur = models.CharField(max_length=200, )
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    csi = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return '%s' % self.reponse_en


class Codecriminel(models.Model):
    reponse_valeur = models.CharField(max_length=200, )
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    violation = models.ForeignKey(Violation, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s' % self.reponse_en

