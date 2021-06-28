from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from rest_framework import permissions
from .serializers import *
from rest_framework import filters
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class ProductsViewSet(viewsets.ModelViewSet):
    
    queryset = Products.objects.all()#.order_by('name')
    serializer_class = ProductsSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    # #permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ['id','name','active','ArticleFamily']#,'active','created_on','last_modified_on','created_by','last_modified_by']
    filterset_fields = ['id','name','active','ArticleFamily']#,'active','created_on','last_modified_on','created_by','last_modified_by']
    

    #http_method_names = ['get', 'post', 'head']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]
    #http_method_names = []

"""
class GroupViewSet(viewsets.ModelViewSet):
    
    #API endpoint that allows groups to be viewed or edited.
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]"""


class CustomersViewSet(viewsets.ModelViewSet):
    queryset = Customers.objects.all()
    serializer_class = CustomersSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ##permission_classes = [permissions.IsAuthenticated]
    ordering_fields =['id','name','email_id', 'contact_number', 'active','address','created_on','last_modified_on','created_by','last_modified_by']
    filterset_fields =['id','name','email_id', 'contact_number', 'active','address','created_on','last_modified_on','created_by','last_modified_by']

class StoresViewSet(viewsets.ModelViewSet):
    queryset = Stores.objects.all()
    serializer_class = StoresSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    #permission_classes = [permissions.IsAuthenticated]
    ordering_fields =['id','name','email_id', 'contact_number', 'active','address','created_on','last_modified_on','created_by','last_modified_by']
    filterset_fields =['id','name','email_id', 'contact_number', 'active','address','created_on','last_modified_on','created_by','last_modified_by']

class ProductStoreViewSet(viewsets.ModelViewSet):
    queryset = Product_Store.objects.all()
    serializer_class = ProductStoreSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    #permission_classes = [permissions.IsAuthenticated]
    ordering_fields =['product_id', 'store_id', 'active', 'custom_product_id','created_on','last_modified_on','created_by','last_modified_by']
    filterset_fields =['product_id', 'store_id', 'active', 'custom_product_id','created_on','last_modified_on','created_by','last_modified_by']

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields =['id','name', 'active','effective_date','end_date','products','store','created_on','last_modified_on','created_by','last_modified_by']
    filterset_fields =['id','name', 'active','effective_date','end_date','products','store','created_on','last_modified_on','created_by','last_modified_by']


class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    http_method_names = ['get', 'post', 'head']
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    ordering_fields =['store','customer','transaction_date','product','amount','price','promotion']
    filterset_fields =['store','customer','transaction_date','product','amount','price','promotion']


class PredictionsViewSet(viewsets.ModelViewSet):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    #permission_classes = [permissions.IsAuthenticated]
    ordering_fields =['customer','product','store','tsnow','tsforecast','prediction_value','prediction_date','prediction_valid_date','model','experiment'] 
    filterset_fields =['customer','product','store','tsnow','tsforecast','prediction_value','prediction_date','prediction_valid_date','model','experiment']

class StagingFolderDataViewSet(viewsets.ModelViewSet):
    queryset = Staging_Folder_Data.objects.all()
    serializer_class = StagingFolderDataSerializer
    filter_backends = [DjangoFilterBackend,filters.OrderingFilter]
    #permission_classes = [permissions.IsAuthenticated]
    ordering_fields =['customer','page','brand','product','discount_type','price_original','price_with_discount','volume','volume_unit','from_date','to_date'] 
    filterset_fields =['customer','page','brand','product','discount_type','price_original','price_with_discount','volume','volume_unit','from_date','to_date']
