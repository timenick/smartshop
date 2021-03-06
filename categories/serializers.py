# Stdlib imports

# Core Django imports

# Third-party app imports
from rest_framework import serializers

# Imports from your apps
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
