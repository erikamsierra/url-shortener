# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from django.views.generic import View
from django.http import Http404
from django.conf import settings
from django.core.cache import cache

from rest_framework import viewsets
from rest_framework.response import Response

from url_shortener.models import ShortenedURL
from url_shortener.serializers import ShortenedURLSerializer
from url_shortener.tasks import update_num_visits


# API views
class ShortenViewSet(viewsets.ViewSet):
    model = ShortenedURL
    serializer = ShortenedURLSerializer

    def create(self, request):
        url_serializer = self.serializer(data=request.data)
        # First we validate if the posted data is correct
        if url_serializer.is_valid():
            # We look for an existing entry or create it if it's a new one
            shortened_url, created = self.model.objects.get_or_create(original_url=url_serializer['url'].value)
            # We add the URL to the cache
            cache.set(shortened_url.short_code, shortened_url.original_url)
            updated_serializer = self.serializer(shortened_url)
            return Response(updated_serializer.data, status=201)
        return Response(url_serializer.errors, status=400)


# Generic Views
class RenderView(View):
    def get(self, request, *args, **kwargs):
        short_code = kwargs.get('short_code')

        #First we try the cache
        original_url = cache.get(short_code)

        # If URL not found in the cache then we try the database
        if not original_url:
            try:
                shortened_url = ShortenedURL.objects.get(short_code=short_code)
            except ShortenedURL.DoesNotExist:
                raise Http404('URL not found: {}'.format(short_code))

            original_url = shortened_url.original_url
            # If URL found in the database, we add it again to the cache
            cache.set(short_code, original_url)

        # Update num_visits asynchronously if tracking enabled
        if settings.TRACK_VISITS:
            update_num_visits.delay(short_code)

        return redirect(original_url)

