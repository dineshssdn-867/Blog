from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from posts.models import Category, Tag, Post


class Archive(models.Model):
    title = models.CharField(_('title'), max_length=150, blank=True, null=True)
    content = models.TextField(_('content'), blank=True, null=True)
    publishing_date = models.DateTimeField(_('publishing_date'), auto_now_add=True, blank=True, null=True,)
    image = models.ImageField(_('image'), blank=True, null=True, upload_to='uploads/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='post_user')
    slug = models.SlugField(_('slug'), default="slug", editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="archives")
    slider_post = models.BooleanField(_('slider_post'), default=False)
    hit = models.PositiveIntegerField(_('hit'), default=0)
    main_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True,  default=1, related_name="posts")

    class Meta:
        ordering = ["id"]
        app_label = 'myarchive'