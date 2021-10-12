from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Category, Comment, Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date', 'status')
    list_filter = ('status', 'date_created', 'pub_date', 'author',)
    search_fields = ('title', 'content',)
    raw_id_fields = ('author',)
    date_hierarchy = 'pub_date'
    ordering = ['status', '-pub_date',]
    readonly_fields = ('slug', 'views', 'count_words', 'read_time', 'likes', 'favourites', 'like_count', 'date_created', 'date_updated')
    actions = ['activate']

    def activate(self, request, queryset):
        queryset.update(status=True)


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    list_display = ('content', 'pub_date', 'status')
    actions = ['activate']

    def activate(self, request, queryset):
        queryset.update(status=True)

admin.site.register(Category)
