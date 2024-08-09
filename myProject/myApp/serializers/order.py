import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from myApp.models import Order, Products


class OrderSerializer(serializers.ModelSerializer):
    totalBill = serializers.SerializerMethodField()
    name = serializers.CharField(source='productId.name', read_only=True)
    price = serializers.DecimalField(max_digits=5, decimal_places=2, source='productId.price', read_only=True)
    user = serializers.CharField(source='userId.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'noOfItems': {'required': True},
            'productId': {'required': True},
            'userId': {'required': True},
            'totalBill': {'write_only': True, 'read_only': True},
            'orderedAt': {'read_only': True},
        }

    def validate_noOfItems(self, item_count):
        if item_count < 1:
            raise serializers.ValidationError({
                'status': 400,
                'message': 'Please select at least one product to place your order.'})
        return item_count

    def get_totalBill(self, obj):
        return obj['noOfItems'] * obj['productId'].price

    def check_inventory(self, obj):
        if obj['noOfItems'] > obj['productId'].inventory:
            items_ = obj['productId'].inventory
            raise serializers.ValidationError({
                'status': 400,
                'message': f'Only {items_} items available, please add no of products only from available stock.',
            })

    def create(self, validated_data):
        self.check_inventory(validated_data)
        validated_data['totalBill'] = self.get_totalBill(validated_data)
        validated_data['orderedAt'] = int(datetime.datetime.now().timestamp())
        product = validated_data.pop('productId')
        user = validated_data.pop('userId')
        order = Order.objects.create(productId=product, userId=user, **validated_data)
        return order

    def to_representation(self, instance):
        representation_ = super(OrderSerializer, self).to_representation(instance)
        representation_.pop('productId')
        representation_.pop('userId')
        representation_.pop('is_removed')
        representation_.pop('price')
        representation_['orderedAt'] = str(datetime.datetime.fromtimestamp(instance.orderedAt))
        representation_['user'] = ' '.join(name.capitalize() for name in instance.userId.username.split('.'))
        return representation_
