from django.contrib import admin

from contact.models import Contact


class AdminPost(admin.ModelAdmin):
    list_filter = ['query']
    list_display = ['name', 'query']
    search_fields = ['name', 'content', 'publishing_date_query']

    class Meta:
        model = Contact
