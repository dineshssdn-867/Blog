from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class Category(models.Model):
    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def post_count(self):
        return self.posts.all().count()

    class Meta:
        ordering = ["id"]


class Tag(models.Model):
    title = models.CharField(_('title'), max_length=50)
    slug = models.SlugField(_('slug'), editable=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def post_count(self):
        return self.posts.all().count()

    class Meta:
        ordering = ["id"]


class Post(models.Model):
    title = models.CharField(_('title'), max_length=150)
    content = models.TextField(_('content'))
    publishing_date = models.DateTimeField(_('publishing_date'), auto_now_add=True)
    image = models.ImageField(_('image'), blank=True, default='/uploads/blog_tckati.jpg', upload_to='uploads/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(_('slug'), default="slug", editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1, related_name="posts")
    tag = models.ManyToManyField(Tag, related_name="posts", blank=True)
    slider_post = models.BooleanField(_('slider_post'), blank=True, null=True)
    hit = models.PositiveIntegerField(_('hit'), default=0)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_post')

    def total_likes(self):
        return self.likes.all().count()

    class Meta:
        ordering = ["id"]

    def comment_count(self):
        return self.comments.all().count()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def post_tag(self):
        return ','.join(str(tag) for tag in self.tag.all())


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'), max_length=100)
    content = models.TextField(_('content'))
    publishing_date = models.DateField(_('publishing_date'), auto_now_add=True)
    image = models.ImageField(_('image'), blank=True, default='users/person-icon-blue-7560_vad8ci.png', upload_to='comment/')

    def __str__(self):
        return self.post.title

    class Meta:
        ordering = ["id"]
