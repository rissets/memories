from modeltranslation.translator import TranslationOptions, register

from .models import *


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
  fields = ('name', 'description')


@register(Post)
class PostTranslationOptions(TranslationOptions):
  fields = ('title', 'excerpt', 'content')
  

