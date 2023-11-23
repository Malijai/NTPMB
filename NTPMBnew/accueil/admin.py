from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Projet, AuditEntree


class RolelInline(admin.StackedInline):
    model = Projet
    can_delete = False
    extra = 1
    min_num = 1


class UserRoleAdmin(UserAdmin):
    inlines = (RolelInline,)
    list_display = ('username', 'email','first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('is_active',)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserRoleAdmin, self).get_inline_instances(request,obj)


@admin.register(AuditEntree)
class AuditEntreeAdmin(admin.ModelAdmin):
    list_display = ['username', 'ip', 'action', 'action_time']
    list_filter = ['action','username']


admin.site.unregister(User)
admin.site.register(User, UserRoleAdmin)


