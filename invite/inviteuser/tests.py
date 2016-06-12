from django.test import TestCase
from inviteuser.models import Invite, DoubleInviteException
from django.contrib.auth.models import User
from django.db import IntegrityError #, DoesNotExist
from django.core.mail import send_mail
from django.core import mail
from inviteuser.views import *
from django.test import Client


class InviteTestCase(TestCase):

    def  setUp(self):
        Invite.objects.create(email="testinvite@gmail.com")
	self.client = Client()


    def test_email(self):
        #just must not fail
        send_mail("Test", "Test text", "test@test.test", ["test2@test.test"], fail_silently=False) 
        

    def test_create_user(self):
        #print "****************************************\n\nTesting create user"	
        invite = Invite.objects.get(email="testinvite@gmail.com")
        user = invite.create_user('bob', '123')
        self.assertEqual(invite.user, user)
        self.assertEqual(invite.email, user.email)
	

    def test_no_double_used_invites(self):
        #print "****************************************\n\nTest can't use the same invite twice"
	
	invite = Invite.objects.create(email="ololo@ololo.lo", value=-1)
	invite.create_user('alice', '123')
	self.assertRaises(DoubleInviteException, invite.create_user, username="kevin", password="123")



    def test_del(self):
	#print "******************************************\n\nTest invite is terminated on deletion of user"

	inv = Invite.objects.create(email="mmmm@mail.com")
	user = User.objects.create_user(username="user", email="mmmm@mail.com", password="123")
        
	inv.user = user
	inv.save()
        user.delete()
	#Invite.objects.get(email="mmm@mail.com")
        self.assertRaises(Invite.DoesNotExist, Invite.objects.get, email="mmm@mail.com")


    def test_create_user_on_invite(self):
        #print "*****************************************\n\n Testing correct user creation via link"          

        invite = Invite.objects.get(email="testinvite@gmail.com")

        response = self.client.get('/invite/%s' % invite.value)

        # Response redirect status code 302
        self.assertEqual(response.status_code, 302)

        invite.refresh_from_db()

        #user was created
        self.assertIsNotNone(invite.user)
        user = User.objects.get(email=invite.email)       
        self.assertEqual(user, invite.user)

        #check correct mail
        self.assertEqual([user.email], mail.outbox[0].to)
        
        #check user authenticated
        self.assertIn('_auth_user_id', self.client.session)         
      

    def test_no_double_used_invite(self):

       #print "****************************************\n\nTesting can't use same invite link twice"
      
       #use invite once
       invite = Invite.objects.get(email="testinvite@gmail.com")
       response = self.client.get('/invite/%s' % invite.value)   

       count_users = len(User.objects.all())

       #empty mailbox
       mail.outbox = []

       #try use invite the second time
       response = self.client.get('/invite/%s' %invite.value)

       self.assertEqual(response.status_code, 200)

       #no mail was send
       self.assertEqual(len(mail.outbox), 0)

       #no new users created
       self.assertEqual(len(User.objects.all()), count_users)


    def test_no_invalid_invite(self):

       #print "************************************************\n\nTesting can't use invalid invite (which does not exist)"

       invite = Invite.objects.get(email="testinvite@gmail.com")
       count_users = len(User.objects.all())

       num = 111
       if num == invite.value:
           num = 112

       #check such invite does not exist
       self.assertRaises(Invite.DoesNotExist, Invite.objects.get, value=num)
       #this invite does not exist 
       response = self.client.get('/invite/%s' % num)

       #not found
       self.assertEqual(response.status_code, 404) 
       #no mail was send
       self.assertEqual(len(mail.outbox), 0)

       #no new users created
       self.assertEqual(len(User.objects.all()), count_users)
 
       #no authentication          
       self.assertNotIn('_auth_user_id', self.client.session)         
 

    def test_logout(self):
       #print "******************************************\n\nTesting logout"
    
       invite = Invite.objects.get(email="testinvite@gmail.com")
       response = self.client.get('/invite/%s' % invite.value)   
      
       self.client.get('/logout/')

       self.assertNotIn('_auth_user_id', self.client.session)         


    def test_login_logout(self):
       #print "******************************************\n\nTesting login/logout"       


       user = User.objects.create_user("bob", "bob@ololo.ru", "123")
       self.client.login(username='bob', password='123')

       self.assertIn('_auth_user_id', self.client.session)         

       response = self.client.get("/")

       self.assertEqual(response.status_code, 200)

       self.client.get("/logout/")

       response =  self.client.get("/")

       self.assertEqual(response.status_code, 302)

       self.assertNotIn('_auth_user_id', self.client.session)         












