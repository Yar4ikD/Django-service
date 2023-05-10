from django.contrib import admin

from account.models import Friend, IncomingRequest, SentRequest

admin.site.register(Friend)
admin.site.register(IncomingRequest)
admin.site.register(SentRequest)
