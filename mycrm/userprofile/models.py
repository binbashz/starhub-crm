from django.contrib.auth.models import User
from django.db import models

from team.models import Team

from django_resized import ResizedImageField




class Userprofile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    active_team = models.ForeignKey(Team, related_name='userprofiles', blank=True, null=True, on_delete=models.CASCADE)
    avatar = ResizedImageField(size=[300, 300], upload_to='avatars/', default='avatars/default.png')

    def get_active_team(self):
        if self.active_team:
            return self.active_team
        else:
            return Team.objects.filter(members__in=[self.user.id]).first()


