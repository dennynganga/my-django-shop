from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

from cart import models, cart_utils

#import checkout_utils

def login(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            pass
        else:
            return render_to_response('billing_shipping_info.html', context_instance=RequestContext(request))
    return HttpResponse('')

def get_user_email(request):
    if request.method == 'POST':
        '''request.session['customer_email'] = request.POST['email']
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"
        buff = BytesIO()
        p = canvas.Canvas(buff)
        p.drawString(100, 100, "Hello World")
        p.showPage()
        p.save()
        doc = SimpleDocTemplate(buff, pagesize=letter)
        Document = []
        doc.build(Document)
        pdf = buff.getvalue()
        buff.close()
        response.write(pdf)
        p = canvas.Canvas(response)
        p.drawString(100, 100, "Hello World")
        p.showPage()
        p.save()'''
        cart = cart_utils.get_or_create_cart(request)
        items = cart.get_items()
        email_subject = 'Your order has been placed'
        email_body = strip_tags(render_to_string('order_email.html', {'items':items}))
        email = EmailMultiAlternatives(email_subject, email_body, 'Logitech Tech <sales@logitech.com>', 
                             (request.session['customer_email'], ), )
        #email.attach('invoice.pdf', pdf, 'application/pdf')
        email.send(fail_silently=False)
        #checkout_utils.set_email(request, customer_email)
    return HttpResponse('')



