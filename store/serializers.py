from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class WilayaInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WilayaInfo
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class OtherSerializer(serializers.ModelSerializer):
    
    price = serializers.IntegerField(required=False, allow_null=True)
    class Meta:
        model = Other
        fields = ['title','price']

class ProductSerializer(serializers.ModelSerializer):
    imgs = ProductImageSerializer(many=True)
    size_or_color = OtherSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','name','price','description','imgs','size_or_color']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'  
        read_only_fields = ['Tracking']