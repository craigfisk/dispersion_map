from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Poll, Choice


def index(request):
#    import pydevd; pydevd.settrace('127.0.0.1')
    """
    output = ""
    if request.user.is_authenticated():
        output += "Authenticated user in HttpRequest object.</P>"
    else:
        output += "Anonymous user in HttpRequest object.</P>"
    """
#    import pdb; pdb.set_trace()
    """
    for item in request.body:
        s += '{0} -- {1}'.format(type(item), item)
    """
    """
    s += 'path: {0}<br/>'.format(request.path)   #str(type(request.REQUEST))
    s += 'host: {0}<br/>'.format(request.get_host())
    s += 'full_path: {0}<br/>'.format(request.get_full_path())
    s += 'secure: {0}<br/>'.format(str(request.is_secure()))
    """
    """
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('polls/index.html')
    c = Context({
        'latest_poll_list': latest_poll_list,
        })
    return HttpResponse(t.render(c))
    """
    """
    output += ', '.join([p.question for p in latest_poll_list])
    return HttpResponse(output)
    """
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list } )

def detail(request, poll_id):

#    import pdb; pdb.set_trace()
#    import sys, os
#    p = sys.path
#    e = os.environ
#    return HttpResponse("You're seeing results of poll %s." % poll_id)
    """
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('polls/detail.html', {'poll': p} )
    """
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p},
            context_instance=RequestContext(request))


def results(request, poll_id):
#    return HttpResponse("Results of poll %s." % poll_id)
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})


def vote(request, poll_id):
#    return HttpResponse("You're going to vote on poll %s." % poll_id)
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # redisplay the poll voting form
        return render_to_response('polls/detail', {
            'poll': p,
            'error_message': "You didn't select a choice.",
            }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # return HttpResponseRedirect after dealing with POST data to prevent data from being posted twice if user hits
        # back button.
        return HttpResponseRedirect(reverse('polls.views.results', args=(p.id,)))

