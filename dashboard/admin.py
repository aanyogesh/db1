from django.contrib import admin
from dashboard.models import *

# Register your models here.

class Staging_Folder_Data_Admin(admin.ModelAdmin):
    list_display = ('customer','page','brand','product','discount_type','price_original','price_with_discount','volume','volume_unit','from_date','to_date')

class TransactionTempAdmin(admin.ModelAdmin):
    list_display = ('id','date','CompositeKey','sales')

class CompositeKeyAdmin(admin.ModelAdmin):
    list_display = ('id','product','store','customer','client')
    
class PredictionsAdmin(admin.ModelAdmin):
    list_display = ('id','product','store','tsnow','tsforecast','prediction_value','prediction_date')

admin.site.register(Products)
admin.site.register(Customers)
admin.site.register(Stores)
admin.site.register(Promotion)
admin.site.register(Transactions)
admin.site.register(Predictions,PredictionsAdmin)
admin.site.register(Product_Store)
admin.site.register(Staging_Folder_Data, Staging_Folder_Data_Admin)
admin.site.register(CompositeKey,CompositeKeyAdmin)
admin.site.register(TransactionTemp,TransactionTempAdmin)

