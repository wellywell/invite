# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from inviteuser.models import Invite, DoubleInviteException
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
import random, string
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from invite.settings import DEFAULT_FROM_EMAIL

# Create your views here.

password  = lambda : ''.join(random.choice(string.letters + string.digits) for _ in range(10))



@login_required
def index(request):

    new = False
    if request.method == 'GET':
	if request.GET.get("new"):
	    new = True


    return render_to_response("index.html", {"username" : request.user.username, "new" : new})
    


def logout_view(request):
    logout(request)
    return redirect("/login/")


def invite(request, num):
    
    try:
        inv = Invite.objects.get(value=num)
    except Invite.DoesNotExist:
        raise Http404()

      
    passw = password()
    uname = "user#" + str(inv.id * 42)       

    try:
	inv.create_user(uname, passw)
    except DoubleInviteException:
	return HttpResponse(u'Этот инвайт уже был использован!')


    send_mail(u'Данные для входа на сайт',
        u'Вы зарегестрированы на сайте. \nЛогин: %s \nПароль: %s' % (uname, passw),
        DEFAULT_FROM_EMAIL,
        [inv.email],
        fail_silently=False)

    user = authenticate(username=uname, password=passw)
    if user is not None:
        if user.is_active:
            login(request, user)

    return redirect("/?new=true")



