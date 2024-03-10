from rest_framework import serializers
from .models import *


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ['created_at', 'updated_at']

