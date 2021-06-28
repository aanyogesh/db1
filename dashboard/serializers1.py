from rest_framework import serializers
from dashboard.models import *
from django.contrib.auth.models import User, Group

class ProductsSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = Products
        #read_only_fields = ('name',)
        #exclude = ('created_by', 'last_modified_by')
        fields = ('id', 'name', 'client_product_description', 'active', 'created_on', 'created_by', 'url', 'last_modified_on', 'last_modified_by')
        #read_only_fields =('name',)
        #def update(self, instance, validated_data):
            #validated_data.pop('name', None)  # prevent myfield from being updated
            #return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
"""class GroupSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = Group
        fields = ['url', 'name']"""

class CustomersSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = Customers
        exclude = ('created_by', 'last_modified_by')

class ProductStoreSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = Product_Store
        exclude = ('created_by', 'last_modified_by')
    def validate(self, data):
        if 'custom_product_id' in data.keys():
            if data['custom_product_id'] =="":
                data['custom_product_id'] = str(data['product_id'])
        else:
            data['custom_product_id'] = str(data['product_id'])
        return data

class PromotionSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = Promotion
        exclude = ('created_by', 'last_modified_by')

class StoresSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    #promo = PromotionSerializer(many=True, read_only=True)
    class Meta:
        model = Stores
        exclude = ('created_by', 'last_modified_by')

class TransactionsSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = Transactions
        exclude = ('created_by', 'last_modified_by')

class PredictionsSerializer(serializers.ModelSerializer):
    id = str(serializers.PrimaryKeyRelatedField(many=True, read_only=True))
    class Meta:
        model = Predictions
        exclude = ('created_by', 'last_modified_by')