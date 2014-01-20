from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import RequestContext, Context
from django.template.loader import render_to_string, get_template
from django.utils.html import strip_tags
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

from cart import models, cart_utils

#import checkout_utils

def checkout(request):
    if request.user.is_authenticated():
        pass
    else:
        return render_to_response('checkout.html', context_instance=RequestContext(request))

def get_user_email(request):
    request.session['customer_email'] = ""
    if request.method == 'POST':
        request.session['customer_email'] = request.POST['shipEmail']
        '''response = HttpResponse(mimetype='application/pdf')
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
        '''template = get_template('order_email.html')
        context = Context({'items':items, 'number':items.count()})
        content = template.render(context)'''
        #text_content = render_to_string('order_email.txt', {'items':items, 'number':items.count()})
        html_content = strip_tags(render_to_string('order_email.html', {'items':items, 'number':items.count()}))
        email = EmailMultiAlternatives(email_subject, html_content, 'Electronix <sales@electronix.com>', 
                             (request.session['customer_email'], ), )
        #email.content_subtype = "html"
        #email.attach_alternative(html_content, 'text/html')
        #email.attach('invoice.pdf', pdf, 'application/pdf')
        email.send(fail_silently=False)
    return HttpResponse('')



