# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
import random, string


class DoubleInviteException(Exception):
    pass


password  = lambda : ''.join(random.choice(string.letters + string.digits) for _ in range(10))




class Invite(models.Model):

    #random identifier
    value = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    @classmethod
    def create(cls, email):
        random.seed()

        #check for collisions
	#Use random numbers so that user knows nothing about their real id in database
        while True:
	    val = random.randint(1, 2147483647)
            invs = Invite.objects.filter(value=val)
	    if len(invs) == 0:
		 break
        invite = cls(value=val, email=email)
	invite.save()
        send_mail(u'Инвайт для регистрации на сайте', u'Поздравляю! Вы получили инвайт! Для регистрации на сайте перейдите по ссылке http://localhost:8000/%s' % invite.value, 'noreply@inviter.com', [invite.email], fail_silently=False)

        return invite

    @classmethod
    def create_user(cls, invite):
	if invite.user != None:
            raise DoubleInviteException("This Invite has been used! The user already exists.")

        passw = password()
        uname = "user#" + str(invite.id * 42)       

        send_mail(u'Данные для входа на сайт',
        u'Вы зарегестрированы на сайте. \nЛогин: %s \nПароль: %s' % (uname, passw),
        'noreply@inviter.com',
        [invite.email],
        fail_silently=False)


	user = User.objects.create_user(username=uname, email=invite.email, password=passw)
	invite.user = user
	invite.save()
	return user
