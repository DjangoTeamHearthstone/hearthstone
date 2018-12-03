from django.contrib import admin
from .models import Card, Exchange, Deck, User_Card, Deck_Card, Profile, Post, Exchange_Card

admin.site.register(Profile)
admin.site.register(Exchange)
admin.site.register(Deck)
admin.site.register(Card)
admin.site.register(User_Card)
admin.site.register(Deck_Card)
admin.site.register(Exchange_Card)
admin.site.register(Post)
# admin.site.register(Fight)

# admin.site.unregister(Exchange)
# admin.site.register(Exchange, AuthTokenAdmin)