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


# class CardOrigin(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     cost = models.IntegerField(null=True)
#     health = models.IntegerField(null=True)
#     attack = models.IntegerField(null=True)
#     text = models.TextField(null=True)

#     def __str__(self):
#         return self.name


# class DeckOrigin(models.Model):
#     name = models.CharField(max_length=200, null=True)
#     cards = ArrayField(
#         ArrayField(
#             models.IntegerField(null=True),
#         ),
#     )
#     cost = models.IntegerField(null=True)

#     def __str__(self):
#         return self.name

class Deck(models.Model):
    user = models.ManyToManyField(User, blank=True)

    name = models.CharField(max_length=200, null=False, default='Nom deck')
    cost = models.IntegerField(null=False, default=0)
    official = models.BooleanField(null=False, default=False)


class Card(models.Model):
    user = models.ManyToManyField(User, blank=True)
    deck = models.ManyToManyField(Deck, blank=True)

    name = models.CharField(max_length=200, null=False, default='Nom carte')
    cost = models.IntegerField(null=False, default=0)
    health = models.IntegerField(null=False, default=0)
    attack = models.IntegerField(null=False, default=0)
    text = models.TextField(null=False, default='Texte carte')
    img = models.CharField(max_length=255, null=False, default='Image carte')

    def __str__(self):
        return self.name


class Exchange(models.Model):
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='creator')
    assignee = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='assignee')

    cards_creator = ArrayField(
        ArrayField(
            models.IntegerField(null=True, blank=True),
        ),
    )

    cards_assignee = ArrayField(
        ArrayField(
            models.IntegerField(null=True, blank=True),
        ),
    )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    title = models.CharField(max_length=200, null=True)
    date = models.DateField(null=True)
    content = models.TextField(null=True)

    def __str__(self):
        return self.title


class Fight(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user')
    opponent = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='opponent')

    health_user = models.IntegerField(null=True)
    health_opponent = models.IntegerField(null=True)
    deck_user = models.IntegerField(null=True)
    deck_opponent = models.IntegerField(null=True)
