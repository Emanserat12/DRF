from decimal import Decimal
from rest_framework import serializers

from myApp.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'description': {'required': True},
            'category': {'required': True},
            'inStock': {'read_only': True},
            'inventory': {'required': True}
        }

    def validate_price(self, price_):
        if price_ < Decimal('1.00') or price_ > Decimal('1000.00'):
            raise serializers.ValidationError('Price has to be between 1.00 and 1000.00')
        return price_

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.category = validated_data.get('category', instance.category)
        instance.inventory = validated_data.get('inventory', instance.inventory)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super(ProductSerializer, self).to_representation(instance)
        representation.pop('id', None)
        representation.pop('is_removed', None)
        return representation
