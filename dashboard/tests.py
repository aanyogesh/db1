from rest_framework import status
from rest_framework.test import APITestCase,APIRequestFactory
from .models import TimeStampedModel,Products
from .serializers import ProductsSerializer
from django.urls import reverse
from json import loads, dumps


class ProductViewsTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.Products = [Products.objects.create() for _ in range(4)]
        cls.product = cls.Products[0]

    def test_can_browse_all_products(self):
        response = self.client.get(reverse("Products:products-list"))
        self.assertEquals(status.HTTP_200_OK, response.status_code)

        response = loads(dumps(response.data))
        res_products =  response['results']
        self.assertEquals(len(self.Products), len(res_products))
        
        for res_product, product in zip(res_products, self.Products):
            self.assertEquals(res_product, ProductsSerializer(instance=product).data)

    def test_can_read_a_specific_product(self):
        response = self.client.get(
            reverse("Products:products-detail", args=[self.product.id])
        )
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(
            ProductsSerializer(instance=self.product).data,
            response.data
        )
    
    def test_can_push_products(self):
        response = self.client.post(reverse("Products:products-list"),{'id':'105'}, format='json')
        self.assertEquals(status.HTTP_201_CREATED, response.status_code )

    def test_can_delete_products(self):
        factory = APIRequestFactory()
        request = factory.delete(reverse("Products:products-list"),{'id':'105'}, format='json')
        response = Products.as_view(request)
        self.assertEquals(status.HTTP_200_OK, request.status_code)