# tests/test_dashbaord.py
import os
import django
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
from dashboard.models import Products

def express_result(prod):
    return {
        'id': prod["id"],
        'name': prod["name"],
        'ArticleFamily': prod["ArticleFamily"],
        'ArticleSubfamily': prod["ArticleSubfamily"],
        'ArticleCategory': prod["ArticleCategory"],
        'active': prod["active"],
    }
    
def express_results(results):
    res = [ express_result(prod) for prod in results ]
    return res

def express_product(prod: Products) -> Dict[str, Any]:
    return {
        'id': prod.id,
        'name': prod.name,
        'ArticleFamily': prod.ArticleFamily,
        'ArticleSubfamily': prod.ArticleSubfamily,
        'ArticleCategory': prod.ArticleCategory,
        'active': prod.active,
    }

express_products = pluralized(express_product)

class TestProductsViewSet(ViewSetTest):
    Products.objects.all().delete()

    list_url = lambda_fixture(
        lambda:
            url_for('products-list'))

    detail_url = lambda_fixture(
        lambda product:
            url_for('products-detail', product.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        products = lambda_fixture(
            lambda: [
                Products.objects.create(
                    name=name,
                    ArticleFamily=ArticleFamily,
                    ArticleSubfamily=ArticleSubfamily,
                    ArticleCategory=ArticleCategory,
                    active=active
                )
                for (name, ArticleFamily, ArticleSubfamily, ArticleCategory, active) in 
                [
                    ("name11", "ArticleFamily1", "ArticleSubfamily1", "ArticleCategory1", True),
                    ("name22", "ArticleFamily2", "ArticleSubfamily2", "ArticleCategory2", False),
                    ("name33", "ArticleFamily3", "ArticleSubfamily3", "ArticleCategory3", False)
                ]
            ],
            autouse=False,
        )
        
        def test_it_returns_values(self, products, results):
            expected = express_products(sorted(products, key=lambda prod: prod.id))
            actual = express_results(results)
            assert expected == actual

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = static_fixture({
            'name': "name4",
            'ArticleFamily': "ArticleFamily4",
            'ArticleSubfamily': "ArticleSubfamily4",
            'ArticleCategory': "ArticleCategory4",
            'active': True,
        })

        initial_product_ids = precondition_fixture(
            lambda:
                set(Products.objects.values_list('id', flat=True)))

        def test_it_creates_new_product(self, initial_product_ids, json):
            json = express_result(json)
            expected = initial_product_ids | {json['id']}
            actual = set(Products.objects.values_list('id', flat=True))
            assert expected == actual

        def test_it_sets_expected_attrs(self, data, json):
            json = express_result(json)
            product = Products.objects.get(pk=json['id'])
            expected = data
            assert_model_attrs(product, expected)

        def test_it_returns_product(self, json):
            json = express_result(json)
            product = Products.objects.get(pk=json['id'])

            expected = express_product(product)
            actual = json
            assert expected == actual


    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        product = lambda_fixture(
            lambda:
                Products.objects.create(
                    name="name4",
                    ArticleFamily="ArticleFamily4",
                    ArticleSubfamily="ArticleSubfamily4",
                    ArticleCategory="ArticleCategory4",
                    active=True
                ))

        def test_it_returns_product(self, product, json):
            expected = express_product(product)
            actual = express_result(json)
            assert expected == actual

    class TestUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        product = lambda_fixture(
            lambda:
                Products.objects.create(
                    name="name4",
                    ArticleFamily="ArticleFamily4",
                    ArticleSubfamily="ArticleSubfamily4",
                    ArticleCategory="ArticleCategory4",
                    active=True
                ))

        data = static_fixture({
            'name': "name4",
            'ArticleFamily': "ArticleFamily4",
            'ArticleSubfamily': "ArticleSubfamily4",
            'ArticleCategory': "ArticleCategory4",
            'active': True,
        })

        def test_it_sets_expected_attrs(self, data, product):
            # We must tell Django to grab fresh data from the database, or we'll
            # see our stale initial data and think our endpoint is broken!
            product.refresh_from_db()

            expected = data
            assert_model_attrs(product, expected)

        def test_it_returns_product(self, product, json):
            product.refresh_from_db()

            expected = express_product(product)
            actual = express_result(json)
            assert expected == actual

    class TestDestroy(
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns204,
    ):
        product = lambda_fixture(
            lambda:
                Products.objects.create(
                    name="name4",
                    ArticleFamily="ArticleFamily4",
                    ArticleSubfamily="ArticleSubfamily4",
                    ArticleCategory="ArticleCategory4",
                    active=True
                ))

        initial_product_ids = precondition_fixture(
            lambda product:  # ensure our to-be-deleted Products exists in our set
                set(Products.objects.values_list('id', flat=True)))

        def test_it_deletes_product(self, initial_product_ids, product):
            expected = initial_product_ids - {product.id}
            actual = set(Products.objects.values_list('id', flat=True))
            assert expected == actual