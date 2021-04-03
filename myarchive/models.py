from django.conf import settings
from django.db import models
# Create your models here.
from posts.models import Category, Tag, Post


class Archive(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    publishing_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, upload_to='uploads/')
    user = models.ForeignKey(Post, on_delete=models.CASCADE)
    slug = models.SlugField(default="slug", editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="archives")
    tag = models.ManyToManyField(Tag, related_name="archives", blank=True)
    slider_post = models.BooleanField(default=False)
    hit = models.PositiveIntegerField(default=0)
    main_user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ,default=None)