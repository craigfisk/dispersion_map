from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from polls.models import Poll, Choice


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form
        return render_to_response('polls/detail', {
            'poll': p,
            'error_message': "You didn't select a choice.",
            }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Return HttpResponseRedirect after dealing with POST data to prevent data 
        # from being posted twice if user hits back button.
        # Also, reverse() can use "poll_results," the optional name given to the 
        # URL in the url() for /vote in polls.urls
        return HttpResponseRedirect(reverse('poll_results', args=(p.id,)))


