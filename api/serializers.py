from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from decimal import Decimal
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Category.objects.all().order_by('id'), source='category', write_only=True
    )
    category = CategorySerializer(read_only=True)

    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'category', 'category_id', 'featured']

        extra_kwargs = {
            'price': {'min_value': Decimal('0.00')},
        }


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all().order_by('id'),
        default=serializers.CurrentUserDefault()
    )
    menuitem = serializers.StringRelatedField()
    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MenuItem.objects.all().order_by('id'), source='menuitem', write_only=True
    )
    unit_price = serializers.DecimalField(source='menuitem.price', read_only=True, max_digits=6, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = models.Cart
        fields = ['id', 'user', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

        validators = [
            UniqueTogetherValidator(
                queryset=models.Cart.objects.all().order_by('id'),
                fields=['user', 'menuitem_id'],
                message='This menu item is already in your cart.'
            )
        ]

        extra_kwargs = {
            'quantity': {'min_value': 1},
        }

    def create(self, validated_data):
        menuitem = validated_data.get('menuitem')
        quantity = validated_data.get('quantity')

        unit_price = menuitem.price
        price = unit_price * quantity

        cart_item = models.Cart.objects.create(
            user=validated_data['user'],
            menuitem=menuitem,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )

        return cart_item


class OrderItemSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Order.objects.all().order_by('id'), source='order', write_only=True
    )
    menuitem = serializers.StringRelatedField()
    menuitem_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MenuItem.objects.all().order_by('id'), source='menuitem', write_only=True
    )
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = models.OrderItem
        fields = ['id', 'order_id', 'menuitem', 'menuitem_id', 'quantity', 'unit_price', 'price']

        validators = [
            UniqueTogetherValidator(
                queryset=models.OrderItem.objects.all().order_by('id'),
                fields=['order', 'menuitem_id'],
                message='This menu item is already in the order.'
            )
        ]

        extra_kwargs = {
            'quantity': {'min_value': 1},
            'unit_price': {'min_value': Decimal('0.00')},
            'price': {'min_value': Decimal('0.00')},
        }


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    delivery_crew = serializers.StringRelatedField(read_only=True)
    delivery_crew_id = serializers.PrimaryKeyRelatedField(
        queryset=models.User.objects.all().order_by('id'), source='delivery_crew', write_only=True, allow_null=True, required=False
    )
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = ['id', 'user', 'delivery_crew', 'delivery_crew_id', 'order_items', 'status', 'total', 'date']
        read_only_fields = ['total', 'delivery_crew']

        extra_kwargs = {
            'total': {'min_value': Decimal('0.00')},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
        read_only_fields = ['email']
