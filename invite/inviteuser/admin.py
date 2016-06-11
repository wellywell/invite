# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import Invite
from django.core.mail import send_mail

@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    fields=('email',)
    
    list_display=('email', 'user')

    def save_model(self, request, invite, *args, **kwargs):
	invite.save()
        send_mail(u'Инвайт для регистрации на сайте', u'Поздравляю! Вы получили инвайт! Для регистрации на сайте перейдите по ссылке http://localhost:8000/%s' % invite.value, 'noreply@inviter.com', [invite.email], fail_silently=False)

