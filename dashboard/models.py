from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.fields import DateField
from django_userforeignkey.models.fields import UserForeignKey
from django.core.validators import RegexValidator
from django.db import IntegrityError
from django.db import transaction
# Create your models here.

class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, null= True, blank=True)
    last_modified_on = models.DateTimeField(auto_now=True, null= True, blank=True)

    class Meta:
        abstract = True

class Products(TimeStampedModel):
    id =models.AutoField(primary_key=True) #BEN code
    name =models.CharField(max_length=80) #description
    ArticleFamily = models.CharField(max_length=200, null= True, blank=True)
    ArticleSubfamily = models.CharField(max_length=200, null= True, blank=True)
    ArticleCategory = models.CharField(max_length=200, null= True, blank=True)
    active = models.BooleanField(default=True)
    #created_on=models.DateTimeField(auto_now_add=True, auto_now=False)
    #last_modified_on=models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name='product_create_by', null= True, blank=True)#models.ForeignKey(User, null=True,blank=True,related_name="products_created_by", on_delete=models.PROTECT)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='product_update_by', null= True, blank=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Products"

class Customers(TimeStampedModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50, unique=False)
    email_id=models.CharField(max_length=50,null= True, blank=True)
    contact_number=models.CharField(max_length=12, blank=True, null=True,)
    active=models.BooleanField(default=True)
    address=models.CharField(max_length=275, null= True, blank=True)
    #created_on=models.DateTimeField(auto_now_add=True, auto_now=False)
    #last_modified_on=models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name='customer_create_by', null= True, blank=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='customer_update_by', null= True, blank=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Customers"

class Stores(TimeStampedModel):
    id=models.AutoField(primary_key=True)
    client_store_description=models.CharField(max_length=250,null= True, blank=True)
    name=models.CharField(max_length=50, unique=False)
    email_id=models.CharField(max_length=50, null= True, blank=True)
    contact_number=models.CharField(max_length=12, null= True, blank=True)
    active=models.BooleanField(default=True)
    address=models.CharField(max_length=300, null= True, blank=True)
    products=models.ManyToManyField(Products, through='Product_Store',related_name="products")
    #created_on=models.DateTimeField(auto_now_add=True, auto_now=False)
    #last_modified_on=models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name='store_create_by', null= True, blank=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='store_update_by', null= True, blank=True)

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Store"

class Product_Store(TimeStampedModel):
  id=models.AutoField(primary_key=True)
  product_id = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='product_ps')
  store_id=models.ForeignKey(Stores, on_delete=models.CASCADE, null= True, blank=True)
  custom_product_id = models.CharField(max_length=25, null=True, blank=True)
  created_by = UserForeignKey(auto_user_add=True, related_name='product_store_create_by', null=True, blank=True)
  last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='product_store_update_by', null=True, blank=True)
  #date_product_was_added = models.DateField(auto_now_add=True, auto_now=False)
  #date_product_was_removed = models.DateField(null=True, blank=True)
  active = models.BooleanField(default=True)
  def save(self, *args, **kwargs):
    try:
      with transaction.atomic():
        if self.custom_product_id is None:
          self.custom_product_id = str(self.product_id)      
        super(Product_Store, self).save(*args, **kwargs)
    except:
      pass
  class Meta:
    unique_together = ('product_id', 'store_id',)

class Promotion(TimeStampedModel):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    promotion_description=models.CharField(max_length=200, blank=False, null=True)
    active=models.BooleanField(default=True)
    effective_date=models.DateField()
    end_date=models.DateField()
    products=models.ManyToManyField(Products)
    store=models.ManyToManyField(Stores, related_name='promo')
    #created_on=models.DateTimeField(auto_now_add=True, auto_now=False)
    #last_modified_on=models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name='promo_create_by',null=True, blank=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='promo_update_by',null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural="Promotion"

"""
'store','customer','transaction_date','product','amount','price','promotion'
"""

class Transactions(TimeStampedModel):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customers, on_delete=models.CASCADE)
    store=models.ForeignKey(Stores, on_delete=models.CASCADE,null=True, blank=True)
    amount=models.FloatField()    #PCS
    price=models.IntegerField(null=True, blank=True)
    promotion=models.BooleanField()#ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True)
    transaction_date=models.DateField(null=False)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    #created_on=models.DateTimeField(auto_now_add=True, auto_now=False)
    #last_modified_on=models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name='trans_create_by',null=True, blank=True)
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='trans_update_by',null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Transaction"
        unique_together = ('transaction_date', 'store','customer','product')

class CompositeKey(models.Model):
    id = models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customers, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    store=models.ForeignKey(Stores, on_delete=models.CASCADE)
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('store','customer','product','client')


class Predictions(TimeStampedModel):
    id=models.AutoField(primary_key=True)
    customer=models.ForeignKey(Customers, on_delete=models.CASCADE)
    product=models.ForeignKey(Products, on_delete=models.CASCADE)
    store=models.ForeignKey(Stores, on_delete=models.CASCADE)
    compositeKey = models.ForeignKey(CompositeKey, on_delete=models.CASCADE)
    tsnow=models.DateField()  #Prediction made on this date for tsforecast date
    tsforecast=models.DateField()  #Prediction made for this date on tsnow
    prediction_value=models.IntegerField()
    prediction_date=models.DateField()  #Prediction script fetched these values on this date
    prediction_valid_date=models.DateField(blank=True, null=True)  
    model=models.CharField(max_length=100)
    experiment=models.CharField(max_length=100)
    #created_on=models.DateTimeField(auto_now_add=True, auto_now=False)
    #last_modified_on=models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = UserForeignKey(auto_user_add=True, related_name='predic_create_by')
    last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='predic_update_by')

    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name_plural="Prediction"
    
class EmailData(TimeStampedModel):
  id=models.AutoField(primary_key=True)
  message_id=models.CharField(max_length=50)
  email_id=models.CharField(max_length=50, blank=False, null=False)
  email_received_date=models.DateTimeField()
  attachment_name=models.CharField(max_length=150)
  attachment_path=models.CharField(max_length=1000)
  processed_dateTime=models.DateTimeField(blank=True,null=True)

class UserConfigs(TimeStampedModel):
  id=models.AutoField(primary_key=True)
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  field_format=models.CharField(max_length=500)
  datatype_format=models.CharField(max_length=500)
  file_regex=models.CharField(max_length=100)
  file_delimiter=models.CharField(max_length=3)
  new_line_delimiter=models.CharField(max_length=3)
  encryption=models.BooleanField(default=False)
  active=models.BooleanField(default=True)
  custom_validation=models.CharField(max_length=100)
  created_by = UserForeignKey(auto_user_add=True, related_name='config_create_by')
  last_modified_by = UserForeignKey(auto_user=True, auto_user_add=True, related_name='config_update_by')

class TransactionTemp(models.Model):
    id=models.ForeignKey(Transactions,on_delete=models.CASCADE, primary_key=True)
    date = models.DateField()
    CompositeKey=models.ForeignKey(CompositeKey,on_delete=models.CASCADE)
    sales=models.IntegerField()
    date_updated = models.DateTimeField()
#store,customer,date,product_id,desc_product,QtyPieces,QtyDelivered,promo,storeName
class Staging(TimeStampedModel):
    id=models.AutoField(primary_key=True)
    store=models.IntegerField( null=True,blank=True)
    storeName = models.CharField(max_length=150, null=True,blank=True)
    customer=models.CharField(max_length=100, null=True,blank=True)
    date=models.DateField(null=True,blank=True)
    product_id=models.IntegerField(null=True,blank=True)
    desc_product=models.CharField(max_length=100, null=True,blank=True)
    QtyPieces=models.FloatField(null=True,blank=True)#qty peices
    QtyDelivered=models.IntegerField(null=True,blank=True)#QtyDelivered
    promo=models.BooleanField(default=False)

class Staging_Folder_Data(models.Model):
  id=models.AutoField(primary_key=True)
  customer=models.CharField(max_length=150, null=True,blank=True)
  page=models.IntegerField(null=True,blank=True)
  brand=models.CharField(max_length=100, null=True,blank=True)
  product=models.CharField(max_length=100, null=True,blank=True)
  discount_type=models.CharField(max_length=100, null=True,blank=True)
  price_original=models.FloatField(null=True,blank=True)
  price_with_discount=models.FloatField(null=True,blank=True)
  volume=models.IntegerField(null=True,blank=True)
  volume_unit=models.CharField(max_length=50,null=True,blank=True)
  from_date=models.DateField(null=True,blank=True)
  to_date=models.DateField(null=True,blank=True)

