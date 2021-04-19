from django.urls import path
from .views import *

app_name = "posts"
urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('myview', MyView.as_view(), name="myview"),
    path('detail/<int:pk>/<slug:slug>', PostDetail.as_view(), name="detail"),
    path('post-update/<int:pk>/<slug:slug>', UpdatePostView.as_view(), name="post_update"),
    path('post-delete/<int:pk>/<slug:slug>', DeletePostView.as_view(), name="post_delete"),
    path('category/<int:pk>/<slug:slug>', CategoryDetail.as_view(), name="category_detail"),
    path('tags/<slug:slug>', TagDetail.as_view(), name="tag_detail"),
    path('post-create', CreatePostView.as_view(), name="create_post"),
    path('search/', SearchView.as_view(), name='search'),
    path('post-add/<int:pk>', CreateArchiveView, name='add-archive'),
    path('detail_archive/<int:pk>/<slug:slug>', PostDetailArchive.as_view(), name="detail_archive"),
    path('detail_like/<int:pk>', post_like, name="like_post")
]
