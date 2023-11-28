from django.contrib import admin
from .models import MBpersonnes
# Register your models here.


class PersonnesAdmin(admin.ModelAdmin):
    model = MBpersonnes
    list_display = ('code', 'completed', 'filecode', 'assistant')
    can_delete = False


admin.site.register(MBpersonnes, PersonnesAdmin)
