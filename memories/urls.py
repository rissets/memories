from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin, sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic.base import TemplateView

from django.views.static import serve

from . import views

handler403 = views.error_403
handler404 = views.error_404
handler500 = views.error_500

sitemaps = {
    'category': views.CategorySitemap,
    'blog': views.PostSitemap,
    # 'tag': views.PortfolioSitemap,
    'static': views.StaticSitemap,
}


urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path("robots.txt", TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]

urlpatterns += i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    # path('', views.home, name='home'),
    path('newsletter/', include('newsletter.urls')),
    path('secret/', admin.site.urls),
    path('account/', include('accounts.urls'), name='accounts'),
    path('account/', include('django.contrib.auth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('pwa.urls')),
    path('', include('blog.urls'), name='blog'),
    # prefix_default_language=False,
    
) 

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
