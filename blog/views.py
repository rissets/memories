from django.contrib import messages
from django.core import serializers
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Q, Sum
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, MonthArchiveView
from meta.views import Meta
from taggit.models import Tag

from memories.mixins import form_errors
import numpy as np
from sklearn import metrics

from .forms import CommentForm, PostSearchForm
from .models import Category, Post
from .utils import get_bert_embeddings, preprocess_text

result = _("Error")
message = _("There was an error, please try again!")


def categories(request):
    categories = Category.objects.exclude(name="default")
    context = {
        'categories': categories,
    }
    return context

class HomeView(ListView):
    model = Post 
    template_name = "blog/index.html"
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status=True).order_by('-pub_date')
    

class PostDetailView(DetailView, Meta):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = 'post'
    comment_form = CommentForm()

    def get_queryset(self):
        return Post.objects.filter(status=True)
    

    def get_context_data(self, **kwargs):
        post = self.model.objects.get(slug=self.kwargs['slug'])
        if post.image:
            meta = Meta(
                title = post.title,
                description = post.excerpt,
                url = post.get_absolute_url(),
                author = post.author.get_full_name(),
                published_time = post.pub_date,
                modified_time = post.date_updated,
                keywords = [tag for tag in post.tags.all()],
                image = post.image.url,
                image_object = {
                    'url': post.image.url,
                    'type': 'some/mime',
                    'width': '100',
                    'height': '100',
                    'alt': post.image_credit
                },
                extra_props = {
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
                },
                extra_custom_props=[
                    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                ],
                use_schemaorg = True,
                use_twitter = True,
                use_og = True,
                use_twitter_tag = True,
                use_facebook = True,
                use_title_tag = True,
            )
        else:
            meta = Meta(
                use_schemaorg = True,
                use_twitter = True,
                use_og = True,
                use_twitter_tag = True,
                use_facebook = True,
                use_title_tag = True,
                title = post.title,
                description = post.excerpt,
                author = post.author.get_full_name(),
                og_author = post.author.get_full_name(),
                published_time = post.pub_date,
                modified_time = post.date_updated,
                keywords = [tag for tag in post.tags.all()],
                
                extra_props = {
                    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0'
                },
                extra_custom_props=[
                    ('http-equiv', 'Content-Type', 'text/html; charset=UTF-8'),
                ],
                
            )

        session_key = f"viewed_article {self.object.slug}"
        if not self.request.session.get(session_key, False):
            self.object.views += 1
            self.object.save()
            self.request.session[session_key] = True

        fav = bool
        if post.favourites.filter(id=self.request.user.id).exists():
            fav = True

        like = bool
        if post.likes.filter(id=self.request.user.id).exists():
            like = True

        allcomments = post.comments.filter(status=True)
        
        page = self.request.GET.get('page', 1)
        paginator = Paginator(allcomments, 4)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        user_comment = None
        
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context['meta'] = meta
        context["fav"] = fav
        context["like"] = like
        context["post"] = post
        context["allcomments"] = allcomments
        context["comments"] = comments
        context["comment_form"] = self.comment_form
        context["related_posts"] = self.model.objects.filter(category=self.object.category, status=True).order_by('?')[:5]
        return context

    def get_related_activities(self):
        queryset = self.object.activity_rel.all()
        paginator = Paginator(queryset, 3)  # paginate_by
        page = self.request.GET.get('page')
        activities = paginator.get_page(page)
        return activities

    def post(self, request, *args, **kwargs):
        post = self.model.objects.get(slug=self.kwargs['slug'])
        new_comment = None
        self.comment_form = CommentForm(request.POST)
        if self.comment_form.is_valid():
            
            if self.request.is_ajax():
                new_comment = self.comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()

                self.object = self.get_object()
                context = super(DetailView, self).get_context_data(**kwargs)
                context['comment_form'] = self.comment_form
                if new_comment is not None:
                    result = "Success"
                    message = _("Thank you! your comments will be approved by us immediately.")
                else:
                    message = form_errors(self.comment_form)
                data = {'result': result, 'message': message}
                return JsonResponse(data)
            new_comment = self.comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

            self.object = self.get_object()
            context = super(DetailView, self).get_context_data(**kwargs)
            context['comment_form'] = self.comment_form
            messages.success(self.request, _("Thank you! Your comments will be approved by us immediately."))
            return redirect(request.META['HTTP_REFERER'])


class CategoryView(ListView, Meta):
    model = Post
    template_name = "blog/category.html"
    context_object_name = "catlist"
    paginate_by = 10

    def get_queryset(self):
        category = self.kwargs['category']
        return self.model.objects.filter(category__name=category).filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        popular = self.model.objects.filter(status=True, pub_date__range=[timezone.now() - timezone.timedelta(15), timezone.now()]).annotate(Sum('views')).order_by('-views')[:3]
        context = super().get_context_data(**kwargs)
        context['popular_list'] = popular
        context['allcategories'] = Category.objects.all().annotate(posts_count=Count('post'))
        context['tags'] = Tag.objects.all()
        context['title'] = self.kwargs['category']
        context['all_posts'] = self.model.objects.order_by('pub_date')
        category = Category.objects.get(name=self.kwargs['category'])
        meta = Meta(
            title = category.name,
            description = category.description,
            use_schemaorg = True,
            use_twitter = True,
            use_og = True,
            use_twitter_tag = True,
            use_facebook = True,
            use_title_tag = True,
        )
        context['meta'] = meta
        return context


def post_search(request):
    form = PostSearchForm()
    q = ''
    # c = ''
    # results = []
    # query = Q()
    #
    # if request.POST.get('action') == 'post':
    #     search_string = str(request.POST.get('ss'))
    #
    #     if search_string is not None:
    #         search_string = Post.objects.filter(title__contains=search_string)[:3]
    #
    #         data = serializers.serialize('json', list(search_string), fields=('id', 'title', 'slug'))
    #
    #         return JsonResponse({'search_string': data}, safe=False)
    #
    # if 'q' in request.GET:
    #     form = PostSearchForm(request.GET)
    #     if form.is_valid():
    #         q = form.cleaned_data['q']
    #         c = form.cleaned_data['c']
    #
    #         if c is not None:
    #             query &= Q(category=c)
    #         if q is not None:
    #             query &= Q(title__contains=q)
    #         # django api refrence
    #         results = Post.objects.filter(query)

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']
        query_text = q

        posts = Post.objects.all()
        encodings = posts.values_list('encodings', flat=True)
        # encodings = encodings.apply(lambda x: np.fromstring(x.strip('[]'), sep=' '))
        encodings = [np.fromstring(x.strip('[]'), sep=' ') for x in encodings]

        query_text = preprocess_text(query_text)
        print(query_text)
        query_encoding = get_bert_embeddings(query_text)

        # similarity_score = encodings.apply(
        #     lambda x: metrics.pairwise.cosine_similarity(x.reshape(1, -1), query_encoding.reshape(1, -1))[0][0])

        similarity_scores = [
            metrics.pairwise.cosine_similarity(encoding.reshape(1, -1), query_encoding.reshape(1, -1))[0][0]
            for encoding in encodings
        ]

        results = list(zip(posts, similarity_scores))

        # Sort the results based on similarity scores
        results = sorted(results, key=lambda x: x[1], reverse=True)


    return render(request, 'blog/search.html', {'form':form,'q':q, 'results':results })


class TagArticlesListView(ListView):
    """
        List posts related to a tag.
    """
    model = Post
    paginate_by = 10
    context_object_name = 'posts_taglist'
    template_name = 'blog/tag_posts_list.html'

    def get_queryset(self):
        """
            Filter Posts by tag_name
        """

        tag_name = self.kwargs.get('tag_name', '')

        if tag_name:
            tag_articles_list = self.model.objects.filter(tags__name__in=[tag_name], status=True).order_by('-pub_date')
            return tag_articles_list
    
    def get_context_data(self, **kwargs):
        popular = self.model.objects.filter(status=True, pub_date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]).annotate(Sum('views')).order_by('-views')[:3]
        context = super().get_context_data(**kwargs)
        context['popular_list'] = popular
        context['allcategories'] = Category.objects.all().annotate(posts_count=Count('post'))
        context['tags'] = Tag.objects.all()
        context['title'] = self.kwargs['tag_name']
        context['all_posts'] = self.model.objects.order_by('pub_date')
        tag = Tag.objects.get(name=self.kwargs['tag_name'])
        meta = Meta(
            title = tag.name,
            use_schemaorg = True,
            use_twitter = True,
            use_og = True,
            use_twitter_tag = True,
            use_facebook = True,
            use_title_tag = True,
        )
        context['meta'] = meta
        return context


class ArticleMonthArchiveView(MonthArchiveView):
    model = Post
    queryset = Post.objects.all()
    date_field = "pub_date"
    allow_future = True
    month_format='%m'
    year_format='%Y'
    template_name = 'blog/archive.html'
    paginate_by = 10

    def get_month(self):
        try:
            month = super(ArticleMonthArchiveView, self).get_month()
        except Http404:
            month = timezone.now().strftime(self.get_month_format())

        return month

    def get_year(self):
        try:
            year = super(ArticleMonthArchiveView, self).get_year()
        except Http404:
            year = timezone.now().strftime(self.get_year_format())

        return year

    def get_context_data(self, **kwargs):
        popular = self.model.objects.filter(status=True, pub_date__range=[timezone.now() - timezone.timedelta(7), timezone.now()]).annotate(Sum('views')).order_by('-views')[:3]
        context = super().get_context_data(**kwargs)
        context['popular_list'] = popular
        context['allcategories'] = Category.objects.all().annotate(posts_count=Count('post'))
        context['tags'] = Tag.objects.all()
        context['all_posts'] = self.model.objects.order_by('pub_date')
        return context
