from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from contact.models import Contact
from django.core.mail import send_mail

class ContactView(TemplateView):
    template_name = "contact/contact.html"


def submit_query(request):
    contact = Contact()
    contact.name = request.POST.get('name')
    contact.email = request.POST.get('email')
    contact.subject = request.POST.get('subject')
    contact.query = request.POST.get('message')
    contact.resolved = False
    contact.save()
    message = """Subject:  """ + contact.subject \
              + """ Dear """ + contact.name + """
    
        Thank you for letting us know about your issue and sorry for inconvenience. We will surely get back to you as soon as possible and also thank you for
        using our services.
         
        Yours sincerely 
        D's Blog Team
    """
    send_mail(contact.subject, message, 'dinesh.n@ahduni.edu.in', [contact.email])
    return redirect('/')
