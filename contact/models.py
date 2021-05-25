from django.db import models
from django.utils.translation import ugettext_lazy as _


class Contact(models.Model):
    name = models.CharField(_('name'), max_length=200)
    email = models.EmailField(_('email'), max_length=254)
    subject = models.CharField(_('subject'), max_length=200)
    query = models.TextField(_('query'))
    publishing_date_query = models.DateTimeField(_('publishing_date_query'), auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.subject
