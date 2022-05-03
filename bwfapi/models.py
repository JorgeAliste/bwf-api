from django.contrib.auth.models import User
from django.db import models


def upload_path_handler(instance, filename):
    return f'avatar/{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE)  # Maybe this could be done with custom User model
    image = models.ImageField(upload_to=upload_path_handler, blank=True)
    is_premium = models.BooleanField(default=False)
    bio = models.CharField(max_length=256, blank=True, null=True)


class Group(models.Model):
    name = models.CharField(max_length=32, null=False, unique=False)
    location = models.CharField(max_length=32, null=False, unique=False)
    description = models.CharField(max_length=256, null=False, unique=False)

    class Meta:
        unique_together = (('name', 'location'),)


class Event(models.Model):
    team_1 = models.CharField(max_length=32, blank=False)
    team_2 = models.CharField(max_length=32, blank=False)
    time = models.DateTimeField(null=False, blank=False)
    score_1 = models.IntegerField(null=True, blank=True)
    score_2 = models.IntegerField(null=True, blank=True)
    group = models.ForeignKey(Group, related_name='events', on_delete=models.CASCADE)
