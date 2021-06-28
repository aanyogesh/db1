from logging import Manager
from django.db.models import fields
from rest_framework import serializers
from dashboard.models import *
from django.contrib.auth.models import User, Group

class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    #product_ps = ProductStoreSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        #read_only_fields = ('name',)
        # exclude = ('created_by', 'last_modified_by')
        fields = ('id', 'name', 'ArticleFamily', 
            'ArticleSubfamily', 'ArticleCategory', 
            'active', 'created_on', 'last_modified_on')
        #read_only_fields =('name',)
        #def update(self, instance, validated_data):
            #validated_data.pop('name', None)  # prevent myfield from being updated
            #return super().update(instance, validated_data)

class ProductsSerializerVersion1(serializers.HyperlinkedModelSerializer):
    #product_ps = ProductStoreSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        #read_only_fields = ('name',)
        #exclude = ('created_by', 'last_modified_by')
        fields = ('id', 'name', 'ArticleFamily', 'url')
        #read_only_fields =('name',) 
        #def update(self, instance, validated_data):
            #validated_data.pop('name', None)  # prevent myfield from being updated
            #return super().update(instance, validated_data)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']
"""class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']"""

class CustomersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customers
        #exclude = ('created_by', 'last_modified_by')
        fields = ('id', 'name', 'email_id', 'contact_number','active','address', 'created_on', 'last_modified_on')


class StoresSerializer(serializers.HyperlinkedModelSerializer):
    #promo = PromotionSerializer(many=True, read_only=True)
    class Meta:
        model = Stores
        #exclude = ('created_by', 'last_modified_by')
        #fields=('id','name','url','products')
        fields = ('id','client_store_description', 'name', 'email_id', 'contact_number','active','address','products', 'created_on', 'last_modified_on')
    products=ProductsSerializer(many=True,read_only=True)


class PromotionSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductsSerializer(many=True,read_only=True)
    store = StoresSerializer(many=True,read_only=True)
    class Meta:
        model = Promotion
        fields = ('id', 'name', 'promotion_description', 'store','active','products', 'created_on', 'last_modified_on')
        #exclude = ('created_by', 'last_modified_by')



class ProductStoreSerializer(serializers.HyperlinkedModelSerializer):
    product_id = ProductsSerializer(read_only=True)
    store_id = StoresSerializer(read_only=True)
    class Meta:
        model = Product_Store
        # exclude = ('created_by', 'last_modified_by')
        fields = ('id', 'url', 'created_on', 'product_id', 'store_id', 'custom_product_id', 'active', 'created_on', 'last_modified_on')
    def validate(self, data):
        if 'custom_product_id' in data.keys():
            if data['custom_product_id'] =="":
                data['custom_product_id'] = str(data['product_id'])
        else:
            data['custom_product_id'] = str(data['product_id'])
        return data

class TransactionsSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductsSerializer(read_only=True)
    customer = CustomersSerializer(read_only=True)
    store = StoresSerializer(read_only=True)
    class Meta:
        model = Transactions
        fields = ('id', 'customer', 'store', 'amount', 'price', 'promotion', 'transaction_date', 'product', 'created_by','last_modified_by')

        #exclude = ('created_by', 'last_modified_by')

class PredictionsSerializer(serializers.HyperlinkedModelSerializer):
    product = ProductsSerializer(read_only=True)
    customer = CustomersSerializer(read_only=True)
    store = StoresSerializer(read_only=True)
    class Meta:
        model = Predictions
        exclude = ('created_by', 'last_modified_by','compositeKey')
        #fields = ('customer','product','store')

class StagingFolderDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Staging_Folder_Data
        fields = ('id','customer','page','brand','product','discount_type','price_original','price_with_discount','volume','volume_unit','from_date','to_date')