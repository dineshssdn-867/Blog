from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


#@method_decorator(cache_page(60 * 15), name='dispatch')
class ContactView(TemplateView):
    template_name = "contact/contact.html"
