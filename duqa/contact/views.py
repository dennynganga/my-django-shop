from django.shortcuts import render_to_response
from django.template import RequestContext

def contact(request):
    return render_to_response("contact.html", context_instance=RequestContext(request))
