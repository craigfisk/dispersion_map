from django.test import TestCase
#from django.test.client import Client
from django.test import Client

from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from forum.models import *

from django.core.urlresolvers import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import time

class SimpleTest(TestCase):
    def setUp(self):
        f = Forum.objects.create(title="forum")
        u = User.objects.create_user("ak", "ak@abc.org", "pwd")
        Site.objects.create(domain="test.org", name="test.org")
        t = Thread.objects.create(title="thread", creator=u, forum=f)
        p = Post.objects.create(title="post", body="body", creator=u, thread=t)
        new_title = p.title

    def content_test(self, url, values):
        """Get content of url and test that each of items in `values` list is present."""
        r = self.c.get(url)
        self.assertEquals(r.status_code, 200)
        for v in values:
            self.assertTrue(v in r.content)

    def test(self):
        self.c = Client()
        self.c.login(username="ak", password="pwd")

        self.content_test("/forum/", ['<a href="/forum/forum/1/">forum</a>'])
        self.content_test("/forum/forum/1/", ['<a href="/forum/thread/1/">thread</a>', "ak - post"])

        self.content_test("/forum/thread/1/", ['<div class="ttitle">thread</div>', '<span class="title">post</span>', 'body <br />', 'by ak |'])
        # '<div class="ttitle">thread</div>' , '<span class="title">post</span>' , 'body <br />', 'by ak |'
        r = self.c.post("/forum/new_thread/1/", {"subject": "thread2", "body": "body2"})
        r = self.c.post("/forum/reply/2/", {"subject": "post2", "body": "body3"})
        self.content_test("/forum/thread/2/", ['<div class="ttitle">thread2</div>',
               '<span class="title">post2</span>', 'body2 <br />', 'body3 <br />'])

        # new_thread
        r = self.c.get("/forum/forum/1/")
        r = self.c.get("/forum/post/new_thread/1")
        r = self.c.post("/forum/post/new_thread/1/", {"subject": "topci", "body" : "Waiting for content"} )
        self.content_test("/forum/forum/1/", ['<div class="title"><a href='])
        """
        # reply
        r = self.c.get("/forum/forum/1/")
        r = self.c.get("/forum/thread/1/")
#        r = self.c.get("/forum/post/reply/1/")

        r = self.c.post("/forum/post/reply/1/", {"subject" : "Re: thread", "body" : "Dogfood"} )
        self.content_test("/forum/thread/1/", ['Dogfood'])
        """





"""
class ForumTest(TestCase):
    def test_main(self):
        self.c = Client()
        self.c.login(username="ak", password="pwd")
        resp = self.c.get('/forum/', {'username': 'ak', 'password': 'pwd'})
        print "After getting forum, resp is: %s" % (resp)
        #self.assertRedirects(resp, '/forum/.*')

    def test_post(self):
        self.c = Client()
        self.c.login(username="ak", password="pwd")
        resp = self.c.get('/forum/post/new_thread/', {'ptype': 'new_thread', 'pk': '10' } )
        print "After getting post, resp is: %s" % (resp)
 
        resp = self.c.post('/forum/post/new_thread/10/', {'subject': 'Kumquat Cake', 'body': "Is there such a thing?"})
        print "After posting to post, resp is: %s" % (resp)
        self.assertRedirects(resp, '/registration/login/?next=/forum/post/new_thread/10/')

class PostTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_post(self):
        self.driver.post("http://localhost:8000/myfruitcake/", {'username':'lindamagee', 'password':'Sp8rky=4242'})
        self.driver.post("http://localhost:8000/forum/post/new_thread/3/", {'subject':'Rabbits', 'body':"Seems like there are a lot of rabbits running around."})
        print "Trying Firefox driver in Selenium"

    def tearDown(self):
        self.driver.quit


class ForumSeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        #cls.selenium.set_script_timeout(30000)
        super(ForumSeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(ForumSeleniumTests, cls).tearDownClass()

    def testforum(self): 
#        self.selenium.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS)
        self.selenium.implicitly_wait(30)
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        ###driver = webdriver.Firefox()
        ###driver.get("/")    #"http://localhost:8000/"
        #driver.get("http://127.0.0.1:8000/")
        #from self.selenium.webdriver.support.wait import WebDriverWait
        #WebDriverWait(self.selenium, 60).until(
        #        lambda driver: driver.find_element_by_link_text("sign-in"))
        signin_element = self.selenium.find_element_by_link_text("sign-in")
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
        elem_username.send_keys("lindamagee")
        time.sleep(10) 
        elem_password = self.selenium.find_element_by_name('password')
        elem_password.send_keys("Sp8rky=4242")
        
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
        # Get elem for "body" of the post, fill in some text, post it:
        ##elem_reply_body = self.selenium.find_element_by_id('subject')
        ##elem_reply_body.send_keys("Birds and holiday baked goods.")
        elem_reply_body = self.selenium.find_element_by_id('body')
        elem_reply_body.send_keys("Birds are big fans of holiday baked goods.")
        elem_reply_body.submit()

        # Return to page with choice between existing and new thread:
        self.selenium.back()
        self.selenium.back()
        self.selenium.back()
        # Click on "start new discussion"
        self.selenium.find_element_by_id("new_topic").click()
        # fill in the new discussion form:
        elem_new_subject = self.selenium.find_element_by_name("subject")
        elem_new_body = self.selenium.find_element_by_id("body")
        elem_new_subject.send_keys("This is a test")
        elem_new_body.send_keys("This is the body of a test")
        elem_new_body.submit()
        # end

        signout_element = self.selenium.find_element_by_link_text("sign-out")
        signout_element.click()
 
        #self.selenium.close()  # closes the window
        self.selenium.quit()   # exits the driver and closes window

"""
                
