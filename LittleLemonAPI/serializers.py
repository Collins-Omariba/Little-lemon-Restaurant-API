from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal

from .models import MenuItem, Cart, Category, Order, OrderItem


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all)
    class Meta():
        model = MenuItem
        fields = ['id','title','price','featured','category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        model = Category
        fields = ['id','title','slug']


class CartSerializer(serializers.ModelSerializer):
    user  = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),default=serializers.CurrentUserDefault())
    def validate(self, attrs):
        attrs['price'] = attrs['quantity'] * attrs['unit_price']
        return attrs
    class Meta():
        model = Cart
        fields = ['user','menuitem','unit_price','quantity','price']

        extra_kwargs = {
            'price' : {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta():
        model = User
        fields = ['id','email','username']



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta():
        model = OrderItem
        fields = ['order','menuitem','price','quantity']


class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many=True, read_only=True,source='order')
    class Meta():
        model = Order
        fields = ['id','user','status','date','total','orderitem','delivery_crew']