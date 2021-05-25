from django.urls import path
from contact.views import *

app_name = "contact"
urlpatterns = [
    path('', ContactView.as_view(), name="contact"),
    path('submit', submit_query, name="submit_query")
]
