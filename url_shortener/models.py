# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from django.utils.crypto import get_random_string


class ShortenedURL(models.Model):
    """
    Represents an url that has been shortened
    """
    original_url = models.TextField(unique=True, db_index=True)
    short_code = models.CharField(max_length=8, unique=True, db_index=True)
    num_visits = models.IntegerField(default=0)

    # Timestamps
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return u'{} > {}'.format(self.short_code, self.original_url)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = ShortenedURL.generate_code()
        super(ShortenedURL, self).save(*args, **kwargs)

    @property
    def shortened_url(self):
        return '{}/{}'.format(settings.DOMAIN, self.short_code)

    @staticmethod
    def generate_code(length=8):
        new_code = get_random_string(length=length)
        if ShortenedURL.objects.filter(short_code=new_code).exists():
            return ShortenedURL.generate_code(length=length)
        return new_code
