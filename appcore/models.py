from django.contrib.postgres.fields import ArrayField
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

class Deck(models.Model):
    user = models.ManyToManyField(User, blank=True)

    name = models.CharField(max_length=200, null=False, default='Nom deck')
    cost = models.IntegerField(null=False, default=0)
    official = models.BooleanField(null=False, default=False)
    img = models.CharField(max_length=255, null=False, default='Image carte')

class Exchange(models.Model):
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='creator')
    assignee = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='assignee')

class Card(models.Model):
    user = models.ManyToManyField(User, blank=True, through='User_Card')
    deck = models.ManyToManyField(Deck, blank=True, through='Deck_Card')
    exchange = models.ManyToManyField(Exchange, blank=True, through="Exchange_Card")

    name = models.CharField(max_length=200, null=False, default='Nom carte')
    cost = models.IntegerField(null=False, default=0)
    health = models.IntegerField(null=False, default=0)
    attack = models.IntegerField(null=False, default=0)
    text = models.TextField(null=False, default='Texte carte')
    img = models.CharField(max_length=255, null=False, default='Image carte')

    def __str__(self):
        return self.name

class User_Card(models.Model):
    user_key = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    card_key = models.ForeignKey(Card, null=True, on_delete=models.CASCADE)

class Deck_Card(models.Model):
    deck_key = models.ForeignKey(Deck, null=True, on_delete=models.CASCADE)
    card_key = models.ForeignKey(Card, null=True, on_delete=models.CASCADE)

class Exchange_Card(models.Model):
    exchange_key = models.ForeignKey(Exchange, null=True, on_delete=models.CASCADE, related_name='exchange_card')
    card_key = models.ForeignKey(Card, null=True, on_delete=models.CASCADE)
    creator_assignee = models.IntegerField(null=False, default=0)

class Room(models.Model):
    name = models.CharField(max_length=200, null=False, default='Nom room')

class Post(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    room = models.ManyToManyField(Room, blank=True)

    title = models.CharField(max_length=200, null=False, default='Titre post')
    date = models.DateField(null=True)
    content = models.TextField(null=False, default='Contenu post')

    def __str__(self):
        return self.title
