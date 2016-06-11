from django.test import TestCase
from inviteuser.models import Invite, DoubleInviteException
from django.contrib.auth.models import User
from django.db import IntegrityError #, DoesNotExist
from django.core.mail import send_mail
from django.core import mail

class InvitedUserTestCase(TestCase):

    def  setUp(self):
        Invite.create(email="testinvite@gmail.com")


    def test_email(self):
        #just must not fail
        send_mail("Test", "Test text", "test@test.test", ["test2@test.test"], fail_silently=False) 
        

    def test_create_user(self):
        print "****************************************\n\nTesting create user"	
        invite = Invite.objects.get(email="testinvite@gmail.com")
        user = Invite.create_user(invite)
        self.assertEqual(invite.user, user)
        self.assertEqual(invite.email, user.email)
	#sent invite
	print mail.outbox[0].body
	#sent credentials
	print mail.outbox[1].body
	

    def test_no_double_used_invites(self):
        print "****************************************\n\nTest can't use the same invite twice"
	
	invite = Invite.objects.create(email="ololo@ololo.lo", value=-1)
	Invite.create_user(invite)
	self.assertRaises(DoubleInviteException, Invite.create_user, invite)



    def test_del(self):
	print "******************************************\n\nTest invite is terminated on deletion of user"

	inv = Invite.create(email="mmmm@mail.com")
	user = User.objects.create_user(username="user", email="mmmm@mail.com", password="123")
        
	inv.user = user
	inv.save()
        user.delete()
	#Invite.objects.get(email="mmm@mail.com")
        self.assertRaises(Invite.DoesNotExist, Invite.objects.get, email="mmm@mail.com")
         
