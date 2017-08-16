from django.contrib import admin

from url_shortener import models


@admin.register(models.ShortenedURL)
class ShortenedURLAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_url', 'short_code', 'num_visits', 'created', 'updated')
    search_fields = ('original_url', 'short_code')
