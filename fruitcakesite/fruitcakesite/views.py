from django.contrib.auth import logout
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def main_page(request):
    return render_to_response('index.html')

def logout_page(request):
    """
    Log user out and redirect to main page.
    """
    logout(request)
    return HttpResponseRedirect('/')

