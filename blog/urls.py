from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.post_search, name="search"),
    path('<slug>/', views.PostDetailView.as_view(), name='detail'),
    path('category/<str:category>/',  views.CategoryView.as_view(), name='category'),
    path('tag/<str:tag_name>/', views.TagArticlesListView.as_view(), name='tag'),
    path('<int:year>/<int:month>/', views.ArticleMonthArchiveView.as_view(month_format='%m'), name="archive_month"),
]
