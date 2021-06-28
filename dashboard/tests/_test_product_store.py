# tests/test_Product_Store.py
import os
import django
import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Foresightee_Database.test_settings')
django.setup()

from typing import Any, Dict

from pytest_common_subject import precondition_fixture
from pytest_drf import (
    ViewSetTest,
    Returns200,
    Returns201,
    Returns204,
    UsesGetMethod,
    UsesDeleteMethod,
    UsesDetailEndpoint,
    UsesListEndpoint,
    UsesPatchMethod,
    UsesPostMethod,
)
from pytest_drf.util import pluralized, url_for
from pytest_lambda import lambda_fixture, static_fixture
from pytest_assert_utils import assert_model_attrs
from dashboard.models import Products, Product_Store, Stores

mock_product = Products.objects.create(
    name="Prod test name",
    ArticleFamily="ArticleFamily",
    ArticleSubfamily="ArticleSubfamily",
    ArticleCategory="ArticleCategory",
    active=True
)

mock_product1 = Products.objects.create(
    name="Prod test name1",
    ArticleFamily="ArticleFamily1",
    ArticleSubfamily="ArticleSubfamily1",
    ArticleCategory="ArticleCategory1",
    active=True
)

mock_store1 = Stores.objects.create(
    name="Mock store test name",
    client_store_description="mock store test client_store_description",
    email_id="mock@mail.com",
    contact_number="9090909090",
    address="test store address",
    active=True
)

mock_store2 = Stores.objects.create(
    name="Mock store test name1",
    client_store_description="mock store test client_store_description1",
    email_id="mock@mail.com",
    contact_number="9090909090",
    address="test store address",
    active=True
)



def express_result(ps):
    return {
        'id': ps['id'],
        'store_id': mock_store1.id,
        'custom_product_id': ps['custom_product_id']
    }
    
def express_results(results):
    res = [ express_result(ps) for ps in results ]
    return res

def express_prostore(ps: Product_Store) -> Dict[str, Any]:
    return {
        'id': ps.id,
        'store_id': mock_store1.id,
        'custom_product_id': ps.custom_product_id
    }

express_prostore = pluralized(express_prostore)

def create_productstore(custom_product_id, mock_store):
    ps_obj = Product_Store.objects.create(
        custom_product_id=custom_product_id,
        product_id=mock_product,
        store_id=mock_store
        
    )
    
    return ps_obj


class TestProStoreViewSet(ViewSetTest):
    Product_Store.objects.all().delete()

    list_url = lambda_fixture(
        lambda:
            url_for('product_store-list'))

    detail_url = lambda_fixture(
        lambda product_store:
            url_for('product_store-detail', product_store.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):

        
        ps_objs = lambda_fixture(
            lambda: [
                create_productstore(custom_product_id, store_id)
                for (custom_product_id, store_id) in 
                [
                    ("custom_product_id12", mock_store1),
                    ("custom_product_id13", mock_store2),
                ]
            ],
            autouse=False,
        )

        
        def test_it_returns_values(self, ps_objs, results):
            expected = express_prostore(sorted(ps_objs, key=lambda ps: ps.id))
            actual = express_results(results)
            assert expected == actual

        
        

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):

        
        data = static_fixture({
            'store_id':mock_store1.id,
            'product_id':mock_product.id,
            'custom_product_id': "custom_product_id12"
        })

        initial_productstore_ids = precondition_fixture(
            lambda:
                set(Product_Store.objects.values_list('id', flat=True)))

        def test_it_creates_new_productstore(self, initial_productstore_ids, json):
            
            json = express_result(json)
            expected = initial_productstore_ids | {json['id']}
            actual = set(Product_Store.objects.values_list('id', flat=True))
            print("json:",json)
            print("****************"*10)
            print("expected:",expected)
            assert expected == actual

        # def test_it_sets_expected_attrs(self, data, json):
        #     json = express_result(json)
        #     #print("json:",json)
        #     product_store = Product_Store.objects.get(pk=json['id'])
        #     expected = data
            
        #     assert_model_attrs(product_store, expected)

        # def test_it_returns_productstore(self, json):
        #     json = express_result(json)
        #     product_store = Product_Store.objects.get(pk=json['id'])
        #     expected = express_prostore(product_store)
        #     actual = json
        #     assert expected == actual


    # class TestRetrieve(
    #     UsesGetMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    #     product_store = lambda_fixture(
    #         lambda:
    #             Product_Store.objects.create(
    #                 product_id=mock_product,
    #                 store_id=mock_store1,
    #                 custom_product_id= "custom_product_id13"
    #             ))

    #     def test_it_returns_productstore(self, product_store, json):
    #         expected = express_prostore(product_store)
    #         actual = express_result(json)
    #         assert expected == actual

    # class TestUpdate(
    #     UsesPatchMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    #     product_store = lambda_fixture(
    #         lambda:
    #             Product_Store.objects.create(
    #                 product_id=mock_product1,
    #                 custom_product_id= "custom_product_id12",
    #                 store_id=mock_store3,
    #                 

    #             ))

                # data = static_fixture({
                #         'product_id':mock_product1,
                #         'store_id':mock_store3,
                #         'custom_product_id': "custom_product_id12"
                        

                        
                #     })

    #     def test_it_sets_expected_attrs(self, data, product_store):
    #         # We must tell Django to grab fresh data from the database, or we'll
    #         # see our stale initial data and think our endpoint is broken!
    #         Product_Store.refresh_from_db()
    #         expected = data
    #         assert_model_attrs(product_store, expected)

    #     def test_it_returns_productstore(self, product_store, json):
    #         Product_Store.refresh_from_db()
    #         expected = express_prostore(product_store)
    #         actual = express_result(json)
    #         assert expected == actual

    # class TestDestroy(
    #     UsesDeleteMethod,
    #     UsesDetailEndpoint,
    #     Returns204,
    # ):
    #     product_store = lambda_fixture(
    #         lambda:
    #             Product_Store.objects.create(
    #                 product_id=mock_product1,
    #                 custom_product_id= "custom_product_id12",
    #                 store_id=mock_store3,
    #                 

    #             ))

    #     initial_productstore_ids = precondition_fixture(
    #         lambda product_store:  
    #             set(Product_Store.objects.values_list('id', flat=True)))

    #     def test_it_deletes_productstore(self, initial_productstore_ids, product_store):
    #         expected = initial_productstore_ids - {product_store.id}
    #         actual = set(Product_Store.objects.values_list('id', flat=True))
    #         assert expected == actual