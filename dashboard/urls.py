from django.urls import include, path
from django.conf.urls import url
from rest_framework.reverse import reverse
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductsViewSet)
router.register(r'stores', views.StoresViewSet)
router.register(r'customers', views.CustomersViewSet)
router.register(r'promotion', views.PromotionViewSet)
router.register(r'transactions', views.TransactionsViewSet)
router.register(r'predictions', views.PredictionsViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'product_store', views.ProductStoreViewSet)
router.register(r'staging', views.StagingFolderDataViewSet)


#router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]