from string import join
from PIL import Image as PImage
from os.path import join as pjoin

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
#from django.utils.decorators import method_decorator

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.core.context_processors import csrf
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from fruitcakesite.settings import MEDIA_ROOT, MEDIA_URL, WIDTH_AVATAR, WIDTH_FRUITCAKE

from myfruitcake.models import Fruitcake, Shipment, Upload, Like
from forum.models import UserProfile
from forum.views import mk_paginator, UserProfile, profile

from django.views.generic import ListView, TemplateView, FormView

from django import forms

#from django.db import models

from fruitcakesite.settings import DEFAULT_FROM_EMAIL
from django.core.mail import EmailMessage, EmailMultiAlternatives
from datetime import datetime

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
#        exclude = ["posts", "user"]

"""
@login_required
def main(request):
    return HttpResponseRedirect("/myfruitcake/")
#    fruitcake = Fruitcake.objects.all()
#    return render_to_response("myfruitcake/myfruitcake_list.html", dict(fruitcake=fruitcake, user=request.user))
"""

def activity(request, pk):
    #Listing of posts in a thread.
    shipments = Shipment.objects.all().order_by("dt")
    shipments = mk_paginator(request, shipments, 15)
    return render_to_response("myfruitcake/activity.html", add_csrf(request, shipments=shipments, media_url=MEDIA_URL))

class FruitcakeListView(ListView):
#    @method_decorator(login_required)
#    def dispatch(self, *args, **kwargs):
#        return super(FruitcakeListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FruitcakeListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        if self.request.user.id:
            return Fruitcake.objects.filter(uploader=self.request.user)
            # or: popup__startswith='Pick me'
        else:
            return Fruitcake.objects.all()

     
# https://docs.djangoproject.com/en/1.4/topics/forms/modelforms/   
# --> should read the modelforms doc from time to time.  For example: 
# "A subclass of ModelForm can accept an existing model instance as the keyword argument instance; if this is supplied,
# save() will update that instance. If it's not supplied, save() will create a new instance of the specified model"
# --> Especially, read the section "This save() method accepts an optional commit keyword argument, which  ..."
"""
from django.db import models

class MyEmailField(models.EmailField):
    def __init__(self, *args, **kwargs):
        super(MyEmailField, self).__init__(*args, **kwargs)
        self.attrs('is_hidden': False)
"""

class ShipmentForm(ModelForm):
    class Meta:
        model = Shipment
        exclude = ('text',)

    def __init__(self, *args, **kwargs):
        super(ShipmentForm, self).__init__(*args, **kwargs)
        self.fields['sender'].widget = forms.TextInput()
        self.fields['receiver'].widget = forms.TextInput()
        
from django.core.validators import validate_email
import re

class MultiEmailField(forms.Field):
    def to_python(self, value):
        # remove whitespace from the string
        pattern = re.compile('\s')
        value = pattern.sub('', value)
        # normalize to list of strings; return empty list if no input
        if not value:
            return []
        return value.split(',')
    
    def validate(self, value):
        super(MultiEmailField, self).validate(value)
        
        for email in value:
            validate_email(email)
                     
        
class EmailContactForm(forms.Form):
    # see class MultiEmailField above
    email = MultiEmailField()
    
    # set up hidden form fields while keeping required fields, using rych's approach:
    # http://stackoverflow.com/questions/6862250/change-a-django-form-field-to-a-hidden-field
    """
    def __init__(self, *args, **kwargs):
        from django.forms.widgets import HiddenInput
        hide_condition = kwargs.pop('hide_condition', None)
        super(FruitcakeEmailForm, self).__init__(*args, **kwargs)
        if hide_condition: # and self.field != 'receiver':
            self.fields['sender'].widget = HiddenInput()
            self.fields['fruitcake'].widget = HiddenInput()
            self.fields['message'].widget = HiddenInput()
#            self.fields['receiver'].widget = HiddenInput()
#            self.fields['receiver'].is_hidden = False
    """
#    to = forms.EmailField(help_text='A valid email address, please.')

#from django.shortcuts import render
#from django.core.mail import send_mail
from django.core.mail import get_connection
from django.forms.models import inlineformset_factory
from myfruitcake.models import EmailContact
from django.template import RequestContext

#from django.template.loader import render_to_string

testlist = ['shoujigui@gmail.com','friskyfrog@comcast.net','magee@cmnw.org']


def email_fruitcake(request, pk):
    """Create instance of Shipment and associated Addressees and send it as email. 
    1) obtain the fruitcake id from passed in value of pk, the sender from request.user, fill in the message
    (later we'll get it, too, from the form, adding to initial={'message': 'Fruitcake for you! etc.), and a list of 
    email addressees from the form.  2) create an instance of Shipment with m2m create of email addresses using the
    list, and then save all that,(see docs.djangoproject.com "Related Objects Reference") 3) email using
    EmailMultiAlternatives.

    """
    if request.method == 'POST':
        form = EmailContactForm(request.POST)
        #formset = EmailContactFormset(request.POST, instance=shipment)
        if form.is_valid():
            cd = form.cleaned_data # cd['email'] is list of email addresses to send to
            subject = 'Fruitcake for you'
            fruitcake = Fruitcake.objects.get(id=pk)
            #sender = User.objects.get(pk=request.user)
            shipment = Shipment(dt=datetime.now(),fruitcake=fruitcake,sender=request.user, message=subject)
            shipment_id = shipment.save()
            for email in cd['email']:
                emailcontact = shipment.emailcontacts.create(email=email)
            #Note: add an "emailed successfully" column to shipment (T/F) to set at the try below?

            #form.save(commit=False)  # save Shipment instance but wait for save_m2m(), or just:
            #shipment = form.save()

            # the emailing part
            # https://docs.djangoproject.com/en/dev/topics/email/
            # CF20121126 solution: http://stackoverflow.com/questions/7583801/send-mass-emails-with-emailmultialternatives
            connection = get_connection()  #uses smtp server specified in settings.py
            
            text_content = "You may follow your shipment %s of fruitcake %s." % (shipment.id, request.POST['fruitcake'])
            #html_content = render_to_string("<P>You may <b>follow</b> your shipment %s of fruitcake %s.</P>" % (shipment.id, request.POST['fruitcake']) ) 
            html_content = "<P>You may <b>follow</b> your shipment %s of fruitcake %s.</P>" % (shipment.id, request.POST['fruitcake'])  
            msg = EmailMultiAlternatives(subject=subject, text_content=text_content, from_email=sender.email,to=cd['email'].pop(), bcc=cd['email'], connection=connection)
            msg.attach_alternative(html_content, "text/html")
            try:
                # If fail_silently=False, send_mail will raise an smtplib.SMTPException. See the smtplib docs for a list of
                # possible exceptions, all of which are subclasses of SMTPException.
                msg.send(fail_silently=False)
            except Exception, e:
                return HttpResponse(e)

            return HttpResponseRedirect('/myfruitcake/success/')
            #return HttpResponseRedirect("/myfruitcake/%(id)s/?err=success" % {"id":shipment_id})
            #return HttpResponse("check email list: %s" % cd['email'])
        else:
            return HttpResponse('Failed on form.is_valid()')
    else:
        form = EmailContactForm()    # initial={'message': 'Happy fruitcake!'}
        
    return render_to_response('myfruitcake/email.html', add_csrf(request, form=form))
 


    """
#    fruitcake = get_object_or_404(Fruitcake, id=pk)
#    form = FruitcakeEmailForm(request.POST or None)
    form = MyForm(request.POST or None)
    if form.is_valid():
        form.fruitcake_id = pk
#        fruitcake.save()
        return redirect('myfruitcake/success.html')
    return render(request, template_name, {'form':form}) 
    """

"""
class MyFruitcakeListView(ListView):
    template_name = 'myfruitcake_list.html'
    context_object_name = 'myfruitcake_list'
    def get_context_data(self, **kwargs):
        context = super(MyFruitcakeListView, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return Fruitcake.objects.filter(user=self.request.user)
"""

class UploadFruitcakeForm(ModelForm):
    class Meta:
        model = Fruitcake
        exclude = ['uploader', 'shipments', 'uploads', 'source', 'thumbnail']

class LikeForm(ModelForm):
    class Meta:
        model = Like
        exclude = ['dt', 'fruitcake', 'user'] 

@login_required
def upload_file(request):

    if request.method == "POST":

        form = UploadFruitcakeForm(request.POST, request.FILES)
        if form.is_valid():
            pic = form.save(commit=False)
            # resize is a now customization of save() in the class
            # then add the request.user
            pic.uploader = request.user
            pic.save()
            #form.save()
#            return HttpResponseRedirect('/myfruitcake/success/')
            return HttpResponseRedirect('/myfruitcake/')

    else:
        form = UploadFruitcakeForm()

    return render_to_response('myfruitcake/upload.html', add_csrf(request, form=form)) 

def success(request):
    return HttpResponse("Success!")

def add_csrf(request, **kwargs):
    d = dict(user=request.user, **kwargs)
    d.update(csrf(request))
    return d


@staff_member_required
def path(request):
    s= " request.path: %s<br />" % (request.path)
    s+= " request.get_full_path(): %s<br />" % (request.get_full_path() )
    s+= " request.get_host(): %s<br />" % (request.get_host() )
    s+= " request.is_secure(): %s<br />" % (request.is_secure() )
    return HttpResponse(s)

@staff_member_required
def meta(request):
    values = request.META.items()
    values.sort()
    html = []
    for k,v in values:
        html.append('<tr><td>%s</td></tr><tr><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

@staff_member_required
def search_form(request):
    return render_to_response('myfruitcake/search_form.html', {'user': request.user} )

@staff_member_required
def search(request):
    profile = UserProfile.objects.get(user=request.user)
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Please enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            fruitcakes = Fruitcake.objects.filter(popup__icontains=q)
            if len(fruitcakes):
                return render_to_response('myfruitcake/search_results.html', {'fruitcakes': fruitcakes, 'query':q,
                    'user':request.user})
            else:
                errors.append('No results for that search.')

    return render_to_response('myfruitcake/search_form.html', {'errors': errors, 'user': request.user} )



