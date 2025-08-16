from .models import Order, OrderItem
from rest_framework import serializers

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields=['id', 'order', 'product', 'amount', 'created_at', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer()
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'total_price', 'updated_at', 'items']