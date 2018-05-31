# Stdlib imports
# Core Django imports
# Third-party app imports
from rest_framework import serializers
# Imports from your apps
from .models import Merchandise


class MerchandiseListShowInfoSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(max_length=100, allow_blank=True)
    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'brand', 'scale', 'unit', 'producePlace',
                  'originPrice', 'promotionPrice', 'clubPrice', 'code', )


class MerchandiseListAllInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = '__all__'


class OrderListMerchandiseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('name', 'promotionPrice', )


class QueryMerchandiseDetailByBarcodeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('barcode',)


class QueryMerchandiseDetailByBarcodeResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('id', 'code', 'barcode', 'name', 'brand', 'scale', 'factory', 'unit',)


class AddMerchandiseDetailByBarcodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchandise
        fields = ('code', 'barcode', 'name', 'brand', 'scale', 'factory', 'unit',)
