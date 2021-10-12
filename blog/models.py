import datetime

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.utils import timezone
from django.utils.text import Truncator, slugify
from meta.models import ModelMeta
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager

from .utils import count_words, read_time, user_directory_path

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=110)
    description = models.TextField(blank=True)

    def save(self):
        name = self.name.lower()
        self.name = name
        super().save()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"category": self.name})

class Post(ModelMeta, models.Model):

    title = models.CharField(max_length=250,null=False, blank=False)
    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = TaggableManager(blank=True)
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    image_credit = models.CharField(max_length=250, null=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = RichTextUploadingField(config_name='default')
    pub_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)
    likes = models.ManyToManyField(User, related_name='like', blank=True, default=None)
    like_count = models.BigIntegerField(default="0")
    status = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    count_words = models.CharField(max_length=50, default=0)
    read_time = models.CharField(max_length=50, default=0)
    deleted = models.BooleanField(default=False)

    class META:
        unique_together = ("title",)
        ordering = ('-pub_date')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.count_words = count_words(self.content)
        self.read_time = read_time(self.content)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})


class Comment(MPTTModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    content = models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    pub_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    class MPTTMeta:
        order_insertion_by = ['pub_date']

    def __str__(self):
        return self.content

