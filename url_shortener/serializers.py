# -*- coding: utf-8 -*-
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework import serializers

from url_shortener import models


url_validator = URLValidator(schemes=['http', 'https'])

class ShortenedURLSerializer(serializers.ModelSerializer):
    """
    Serializer to represent a ShortenedURL
    """
    url = serializers.CharField(source='original_url')
    shortened_url = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = models.ShortenedURL
        fields = ('url', 'shortened_url')


    @staticmethod
    def validate_url(value):
        # URLValidator doesn't accept URLs without protocol, so we need to add it before validating, if missing
        if not value.startswith('http'):
            value = 'http://{}'.format(value)
        try:
            url_validator(value)
        except ValidationError as e:
            raise e
        return value


