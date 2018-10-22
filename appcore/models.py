from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    treasure = models.IntegerField(default=400)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

    ## error User no profil
    # $ python manage.py shell
    # > from django.contrib.auth.models import User
    # > from appcore.models import Profile
    # > users = User.objects.filter(profile=None)
    # > for user in users:
    # >     Profile.objects.create(user=user)


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    name = models.CharField(max_length=200, null=True)
    cost = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    attack = models.IntegerField(null=True)
    text = models.TextField(null=True)

    def __str__(self):
        return self.name
