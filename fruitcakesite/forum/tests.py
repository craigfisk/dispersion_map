from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from forum.models import *

from django.core.urlresolvers import reverse

from selenium import webdriver

class SimpleTest(TestCase):
    def setUp(self):
        f = Forum.objects.create(title="forum")
        u = User.objects.create_user("ak", "ak@abc.org", "pwd")
        Site.objects.create(domain="test.org", name="test.org")
        t = Thread.objects.create(title="thread", creator=u, forum=f)
        p = Post.objects.create(title="post", body="body", creator=u, thread=t)

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

