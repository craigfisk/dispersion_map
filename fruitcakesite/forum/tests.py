from django.test import TestCase
from django.test.client import Client
from django.test import Client

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from forum.models import Forum, Thread, Post

from django.core.urlresolvers import reverse
import time
from os.path import join as pjoin
from fruitcakesite.settings import MEDIA_ROOT


class ForumPostsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ak', password='pwd', email='ak@justfruitcake.com')
        self.forum = Forum.objects.create(title='Raspberry pie')
        self.thread = Thread.objects.create(title='About raspberry pie', creator=self.user, forum=self.forum)
        self.post = Post.objects.create(title='Re: About raspberry pie', body='Yes (maybe not).', creator=self.user, thread=self.thread)

    def content_test(self, url, values):
        #Get content of url and test that each of items in `values` list is present.
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200) 
        for v in values:
            self.assertTrue(v in r.content)

    def redirect_test(self, url, values):
        #Get content of url and test that each of items in `values` list is present.
        r = self.c.get(url, follow=True)
        self.assertEquals(r.status_code, 200) 
        for v in values:
            self.assertTrue(v in r.content)

    def test_post_new_reply_and_reply_and_upload_avatar(self):
        self.c = Client()
        loggedin = self.c.login(username='ak', password='pwd')
        f = Forum.objects.get(pk=1)
       
        # Check that our test forum exists
        r1 = self.c.get('/forum/')
        self.assertTrue('Raspberry pie' in r1.content)

        # Create a new thread on that forum
        r2 = self.c.get('/forum/post/new_thread/1')
        self.assertEqual(r2.status_code, 200)
        r3 = self.c.post('/forum/post/new_thread/1', {'subject': 'About raspberry pie', 'body': 'Could raspberry pie be considered fruitcake?'}, follow=True)
        self.content_test('/forum/', ['About raspberry pie',])
        #self.c.get('/forum/forum/1')
        self.content_test('/forum/forum/1', ['About raspberry pie',])

        # Reply to a thread (first create the thread)
        t = self.thread
        r4 = self.c.post('/forum/post/reply/1/', {'subject': 'About raspberry pie', 'body': 'Yes (maybe not).'})
        self.content_test('/forum/thread/1/?page=last', ['Yes (maybe not)',])

        # upload avatar
        testavatarpath = 'testavatar.jpg'
        imfn = pjoin(MEDIA_ROOT, testavatarpath)
        r = self.c.get('/forum/upload/', follow=True)

        # test the various unicode methods
        self.assertEqual(self.forum.title, self.forum.__unicode__() )
        self.assertEqual(self.thread.__unicode__(), (str(self.user) + " - " + self.thread.title) )
        self.assertEqual(self.thread.num_replies(), (self.thread.post_set.count() - 1)  )
        self.assertEqual(self.post.__unicode__(), (str(self.post.creator) + ' - ' + str(self.post.thread) + ' - ' + self.post.title) )

"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class ForumTest(TestCase):
    def test_main(self):
        self.c = Client()
        self.c.login(username='ak', password='pwd')
        resp = self.c.get('/forum/', {'username': 'ak', 'password': 'pwd'})
        print "After getting forum, resp is: %s" % (resp)
        #self.assertRedirects(resp, '/forum/.*')

    def test_post(self):
        self.c = Client()
        self.c.login(username='ak', password='pwd')
        resp = self.c.get('/forum/post/new_thread/', {'ptype': 'new_thread', 'pk': '10' } )
        print "After getting post, resp is: %s" % (resp)
 
        resp = self.c.post('/forum/post/new_thread/10/', {'subject': 'Kumquat Cake', 'body': 'Is there such a thing?'})
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
        self.user = User.objects.create_user(username='ak', password='pwd', email='ak@justfruitcake.com')
        self.forum = Forum.objects.create(title='Raspberry pie')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ForumSeleniumTests, cls).tearDownClass()

    def testforum(self): 
#        self.selenium.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
        #self.selenium.implicitly_wait(30)
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        u = User.objects.get(username='ak')
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


