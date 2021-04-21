from cloudinary_storage import storage
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from PIL import Image
from django.db.models.signals import post_save
from posts.models import Category
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_day = models.DateField(_('birth_day'), null=True, blank=True)
    bio = models.TextField(_('bio'), max_length=1000, blank=True)
    image = models.ImageField(_('image'), blank=True, null=True, default='users/person-icon-blue-7560_vad8ci.png', upload_to='users/')
    slug = models.SlugField(_('slug'), editable=False)
    category_like = models.ManyToManyField(Category, default="food")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
