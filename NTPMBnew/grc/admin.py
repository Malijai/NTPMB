from django.contrib import admin
from .models import Personnegrc


class PersonnegrcAdmin(admin.ModelAdmin):
    admin.site.site_header = 'Personnes GRC'
    list_display = ('codeGRC', 'dateprint', 'ferme','RA')
    list_filter = ['province', 'ferme', 'RA', 'codeGRC']

    def save_model(self, request, obj, form, change):
        obj.save()

admin.site.register(Personnegrc, PersonnegrcAdmin)