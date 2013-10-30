from django.test import TestCase
#from django.test.client import Client
from django.test import Client

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from forum.models import Forum, Thread, Post, UserProfile
from forum.views import UserForm, ProfileForm
from forum.urls import *

from django.core.urlresolvers import reverse, resolve
import time
from os.path import join as pjoin
from fruitcakesite.settings import MEDIA_ROOT
import os, re

class ForumPostsTestCase(TestCase):
    def setUp(self):
        print 'Starting setup'
        self.remove_test_files('images', r'3949266199_540cce70e5_.*$')
        self.testavatarsource = 'tests/3949266199_540cce70e5.jpg'
        self.testavatar = 'images/3949266199_540cce70e5.jpg'
        #self.badavatar = 'tests/badavatar.jpg'

        self.user = User.objects.create_user(username='cf', password='pwd', email='cf@justfruitcake.com')

        self.userprofile = UserProfile(avatar=pjoin(MEDIA_ROOT, self.testavatar), posts=0, shipments=0, user=self.user)

        #self.user2 = User.objects.create_user(username='craig', password='pwd', email='craig@justfruitcake.com')
        self.forum = Forum.objects.create(title='Raspberry pie')
        self.thread = Thread.objects.create(title='About raspberry pie', creator=self.user, forum=self.forum)
        self.post = Post.objects.create(title='Re: About raspberry pie', body='Yes (maybe not).', creator=self.user, thread=self.thread)
 

        self.loggedin = self.client.login(username='cf', password='pwd')
        #self.f = Forum.objects.get(pk=1)
 
        print 'Finished setup'

        #self.baduserprofile = UserProfile(avatar=self.badavatar, posts=0, shipments=0, user_id=self.user.id)

    def tearDown(self):
        self.user.delete()
        print 'All done.'

    def remove_test_files(self, subdirectory, pattern):
        somedir = pjoin(MEDIA_ROOT, subdirectory)
        names = os.listdir(somedir)
        f_re = re.compile(pattern)
        for name in names:
            for m in f_re.finditer(name):
                if m: os.unlink( pjoin(somedir, m.group()) )
    
    #def teardown(self):
    #    self.remove_test_files('images', r'3949266199_540cce70e5.*$')

    def content_test(self, url, values):
        #Get content of url and test that each of items in `values` list is present.
        r = self.client.get(url)
        self.assertEquals(r.status_code, 200) 
        for v in values:
            self.assertTrue(v in r.content)

    def redirect_test(self, url, values):
        #Get content of url and test that each of items in `values` list is present.
        r = self.client.get(url, follow=True)
        self.assertEquals(r.status_code, 200) 
        for v in values:
            self.assertTrue(v in r.content)

    def test_post_new_reply_and_reply_and_upload_avatar(self):
        #self.client = Client()
      
        # Check that our test forum exists
        r1 = self.client.get('/forum/')
        self.assertTrue('Raspberry pie' in r1.content)

    def test_get_new_thread(self):
        # Create a new thread on that forum
        r2 = self.client.get('/forum/post/new_thread/1/')
        self.assertEqual(r2.status_code, 200)
        self.content_test('/forum/post/new_thread/1/', ['Start New Topic', ])
        
        #r3 = self.client.post( reverse('forum_post', args=['new_thread', '1']), dict(subject='More desert', body='Yes, please!'))
    
    def test_create_new_thread(self):
        r3 = self.client.post('/forum/new_thread/1', {'subject': 'About raspberry pie', 'body': 'Could raspberry pie be considered fruitcake?'}, follow=True)
        self.content_test('/forum/', ['About raspberry pie',])
        #self.client.get('/forum/forum/1')
        self.content_test('/forum/forum/1', ['About raspberry pie',])
        
        #WHICH OF THESE IS RIGHT?
        m = self.client.post('/forum/post/new_thread/1/', {'subject': 'Some topic', 'body': 'This is the body'} )
        n = self.client.post('/forum/new_thread/1/', {'subject': 'Some topic', 'body': 'This is the body'} )
        
    def test_reply_to_a_thread(self):
        # Reply to a thread (first create the thread)
        #t = self.thread
        ##r4 = self.client.post('/forum/post/reply/1/', {'subject': 'About raspberry pie', 'body': 'Yes (maybe not).'})
        ##self.content_test('/forum/thread/1/?page=last', ['Yes (maybe not)',])
        
        # AGAIN, WHICH IS RICHT?   'subject': 'Re: About raspberry pie', 
        subject = "Re: " + self.thread.title
        thread_id = self.thread.id
        #response = self.client.post('/forum/post/reply/1/', {'subject': subject, 'body': 'Yes (maybe not).'} )
        response = self.client.post( reverse('forum_post', args=('reply',unicode(self.post.id))) , {'subject':subject, 'body':'Yes (maybe not).'} )
        #response = self.client.post( reverse('forum_post', args=('reply', '7')), {'subject':subject, 'body':'Yes (maybe not).'} )##q = self.client.post('/forum/reply/1/', {'subject': 'Some topic', 'body': 'We do not agree'} )
        print response.status_code
        
        response = self.client.get('/forum/thread/' + unicode(thread_id) + '/?=page=last')
        self.assertTrue('Yes (maybe not)' in response.content)
        
        # upload avatar
        #3testavatarpath = 'testavatar.jpg'
        ##imfn = pjoin(MEDIA_ROOT, testavatarpath)
        ##r = self.client.get('/forum/upload/', follow=True)

    def test_unicode_methods(self):
        # test the various unicode methods
        self.assertEqual(self.forum.title, self.forum.__unicode__() )
        self.assertEqual(self.thread.__unicode__(), (str(self.user) + " - " + self.thread.title) )
        self.assertEqual(self.thread.num_replies(), (self.thread.post_set.count() - 1)  )
        self.assertEqual(self.post.__unicode__(), (str(self.post.creator) + ' - ' + str(self.post.thread) + ' - ' + self.post.title) )

    def test_userinfo(self):
        r = self.client.get('/forum/userinfo/' + unicode(self.userprofile.user_id))
        #self.assertEqual(r.status_code, 200)
        #r.content
        print r.status_code
        self.assertEqual(self.userprofile.__unicode__(), unicode(self.user.__unicode__()))
         
        #r5 = self.client.get('/forum/userinfo/'+ unicode(self.userprofile.user_id), {'username':'cf', 'email':'wcraigfisk@gmail.com'} )
        #print r5.status_code
       
    def test_userinfo_via_reverse(self):     
        #----------- 
        response = self.client.get( reverse('forum_userinfo', args=(self.user.id,)))
        #response = self.client.get( reverse('forum_userinfo', args=(1,)))
        self.assertContains(response, 'cf!')

    def test_userinfo_via_reverse_with_args_kwargs(self):
        # Following line gives "don't mix *args and **kwargs in call to reverse".  
        # OK, but how do you pass positional and named arguments at the same time?
        #response = self.client.post( reverse('forum_userinfo', args=(self.userprofile.user.id,), kwargs={'username': self.user, 'email':self.user.email}), follow=True)
        #See https://docs.djangoproject.com/en/1.5/ref/urlresolvers/#https://docs.djangoproject.com/en/1.5/ref/urlresolvers/
        response = self.client.post(reverse('forum_userinfo', args=(self.user.id,)), dict(username=self.user, email= self.userprofile.user.email) )
        #Or: b = self.client.post(reverse('forum_userinfo', args=(1,)), {'username':self.user, 'email':self.userprofile.user.email} )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit My Profile')
       
    def test_profilepic_with_reverse(self):
        response = self.client.get( reverse('forum_profilepic', args=(self.user.id,)))
        self.assertTrue('cf' in response.content)
        print 'hi'
        
    def test_profilepic_with_reverse_and_avatar(self):
        response = self.client.post( reverse('forum_profilepic', args=(unicode(self.user.id),)), dict(avatar=self.userprofile.avatar.name) )
        print response.status_code
        self.assertContains(response, self.userprofile.avatar.name)
        print 'howdy'
        
    """
    def test_profilepic_with_reverse_on_badavatar(self):
        response = self.client.post( reverse('forum_profilepic', args=((self.user.id),)), dict(avatar=self.baduserprofile.avatar) )
        print response.status_code
        print 'hi there'
        self.assertContains(response, self.userprofile.avatar.name)
        self.assertEqual(response.status_code, 200)
    """

"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ForumTest(TestCase):
    def test_main(self):
        self.client = Client()
        self.client.login(username='cf', password='pwd')
        resp = self.client.get('/forum/', {'username': 'cf', 'password': 'pwd'})
        print "After getting forum, resp is: %s" % (resp)
        #self.assertRedirects(resp, '/forum/.*')

    def test_post(self):
        self.client = Client()
        self.client.login(username='cf', password='pwd')
        resp = self.client.get('/forum/post/new_thread/', {'ptype': 'new_thread', 'pk': '10' } )
        print "After getting post, resp is: %s" % (resp)
 
        resp = self.client.post('/forum/post/new_thread/10/', {'subject': 'Kumquat Cake', 'body': 'Is there such a thing?'})
        print "After posting to post, resp is: %s" % (resp)
        self.assertRedirects(resp, '/registration/login/?next=/forum/post/new_thread/10/')

class PostTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_post(self):
        self.driver.post('http://localhost:8000/myfruitcake/', {'username':'lindamagee', 'password':'Sp8rky=4242'})
        self.driver.post('http://localhost:8000/forum/post/new_thread/3/', {'subject':'Rabbits', 'body':'Seems like there are a lot of rabbits running around.'})
        print "Trying Firefox driver in Selenium"

    def tearDown(self):
        self.driver.quit

class ForumSeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        #cls.selenium.set_script_timeout(30000)
        super(ForumSeleniumTests, cls).setUpClass()

    def setUp(self):
        self.user = User.objects.create_user(username='cf', password='pwd', email='cf@justfruitcake.com')
        self.forum = Forum.objects.create(title='Raspberry pie')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ForumSeleniumTests, cls).tearDownClass()

    def testforum(self): 
#        self.selenium.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
        #self.selenium.implicitly_wait(30)
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        u = User.objects.get(username='cf')
        f = Forum.objects.get(pk=1)
        
        driver = webdriver.Firefox()
        driver.get('/')    #'http://localhost:8000/'
        #driver.get('http://127.0.0.1:8000/')
        #from self.selenium.webdriver.support.wait import WebDriverWait
        #WebDriverWait(self.selenium, 60).until(
        #        lambda driver: driver.find_element_by_link_text('sign-in'))
        signin_element = self.selenium.find_element_by_link_text('sign-in')
        signin_element.click()
        # signin_element.tag_name --> u'a'
        # signin_element.text --> u'sign-in'
        ###signin_elem.click()   # goes to the sign-in page
        # where username and password are the names of the form fields to fill in:
        #WebDriverWait(self.selenium, 60).until(
        #        lambda driver: driver.find_element_by_name('password'))
        time.sleep(10)
        elem_username = self.selenium.find_element_by_name('username')
        # send the text to the form:
        elem_username.send_keys('lindamagee')
        time.sleep(10) 
        elem_password = self.selenium.find_element_by_name('password')
        elem_password.send_keys('Sp8rky=4242')
        
        elem_password.submit()          # bubbles up to the form and submits it

        # go to Forum
        elem_forum = self.selenium.find_element_by_name('forum')
        elem_forum.click()
        # go to a forum
        self.selenium.find_element_by_link_text('Fruitcake tradition').click()
        # go to a thread
        self.selenium.find_element_by_link_text('Holiday baking for pet birds').click()
        # Reply to create another post in the thread
        self.selenium.find_element_by_link_text('Reply').click()
        # Get elem for 'body' of the post, fill in some text, post it:
        ##elem_reply_body = self.selenium.find_element_by_id('subject')
        ##elem_reply_body.send_keys('Birds and holiday baked goods.')
        elem_reply_body = self.selenium.find_element_by_id('body')
        elem_reply_body.send_keys('Birds are big fans of holiday baked goods.')
        elem_reply_body.submit()

        # Return to page with choice between existing and new thread:
        self.selenium.back()
        self.selenium.back()
        self.selenium.back()
        # Click on 'start new discussion'
        self.selenium.find_element_by_id('new_topic').click()
        # fill in the new discussion form:
        elem_new_subject = self.selenium.find_element_by_name('subject')
        elem_new_body = self.selenium.find_element_by_id('body')
        elem_new_subject.send_keys('This is a test')
        elem_new_body.send_keys('This is the body of a test')
        elem_new_body.submit()
        # end

        signout_element = self.selenium.find_element_by_link_text('sign-out')
        signout_element.click()
        #self.selenium.close()  # closes the window
        self.selenium.quit()   # exits the driver and closes window
"""


