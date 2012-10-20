from django.shortcuts import render_to_response
#from django.http import HttpResponseRedirect
#from django.contrib.auth.decorators import login_required

def accounts_home(request):
    return render_to_response('index.html')

