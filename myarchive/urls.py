from django.urls import path
from myarchive.views import ArchiveView

app_name = "archive"
urlpatterns = [
    path('', ArchiveView.as_view(), name="archive"),
]
