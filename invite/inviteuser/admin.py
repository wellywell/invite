# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Invite
from django.core.mail import send_mail
from invite.settings import HOSTNAME, DEFAULT_FROM_EMAIL

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    fields=('email',)
    
    list_display=('email', 'user', 'value')

    def save_model(self, request, invite, *args, **kwargs):
	#when new invite is created, send mail
	if invite.value == None:
	    invite.save()
            send_mail(u'Инвайт для регистрации на сайте', u'Поздравляю! Вы получили инвайт! Для регистрации на сайте перейдите по ссылке http://%s/invite/%s' % (HOSTNAME, invite.value), DEFAULT_FROM_EMAIL, [invite.email], fail_silently=False)

