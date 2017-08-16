"""url_shortener URL Configuration"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from url_shortener import views


short_code = r'(?P<short_code>[a-zA-Z0-9]{8})'

# API URLs
router = routers.DefaultRouter()
router.register(r'shorten_url', views.ShortenViewSet, base_name='shorten_url')


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^{}'.format(short_code), views.RenderView.as_view()),
    url(r'', include(router.urls))
]