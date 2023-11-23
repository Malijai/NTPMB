from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

##Pour les utilisateurs
class Projet(models.Model):
    NTPMB = 1
    GRCMB = 2
    ALL = 10
    PROJETS_CHOICES = (
                           (NTPMB, 'National Trajectory Project'),
                           (GRCMB, 'GRC MB Replication'),
                           (ALL, 'All projects'),
                        )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    projet = models.PositiveSmallIntegerField(choices=PROJETS_CHOICES, verbose_name="Projets", null=True, blank=True)

    def __str__(self):
        return self.user.username


##Pour le logging
class AuditEntree(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)
    action_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


def user_action_callback(sender, request, username, **kwargs):
    user_action = kwargs.get('user_action')
    ip = request.META.get('REMOTE_ADDR')
    AuditEntree.objects.create(action=user_action, ip=ip, username=username)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    user_action_callback(sender, request, user.username, user_action='user_logged_in')


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    user_action_callback(sender, request, user.username, user_action='user_logged_out')


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    user_action_callback(sender, request, credentials.get('username', None), user_action='login_failed')
