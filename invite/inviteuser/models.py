# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
import random, string


class DoubleInviteException(Exception):
    pass

class Invite(models.Model):

    #random identifier
    value = models.IntegerField(unique=True)
    email = models.EmailField(unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
	if self.value == None:
	    self.value = Invite.hash()
        super(Invite, self).save(*args, **kwargs) 


    def create_user(self, username, password):
	if self.user != None:
            raise DoubleInviteException("This Invite has been used! The user already exists.")

	user = User.objects.create_user(username=username, email=self.email, password=password)
	self.user = user
	self.save()
	return user

    @classmethod
    def hash(cls):

        random.seed()
        #check for collisions
	#Use random numbers so that user knows nothing about their real id in database
        while True:
	    val = random.randint(1, 2147483647)
            invs = Invite.objects.filter(value=val)
	    if len(invs) == 0:
		 break
	return val

