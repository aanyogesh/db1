# tests/test_stage.py
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
from dashboard.models import Staging_Folder_Data



def express_result(stage):
    print("STAGE:::", stage)

    return {
        'id': stage["id"],
        'customer': stage["customer"],
        'page':stage["page"],
        'brand':stage["brand"],
        'product':stage["product"],
        'discount_type':stage["discount_type"],
        'price_original':stage["price_original"],
        'price_with_discount':stage["price_with_discount"],
        'volume':stage["volume"],
        'volume_unit':stage["volume_unit"]
        
    }
    
def express_results(results):
    res = [ express_result(stage) for stage in results ]
    return res

def express_stg(stage: Staging_Folder_Data) -> Dict[str, Any]:
    return {
        'id': stage.id,
        'customer': stage.customer,
        'page': stage.page,
        'brand': stage.brand,
        'product': stage.product,
        'discount_type': stage.discount_type,
        'price_original': stage.price_original,
        'price_with_discount': stage.price_with_discount,
        'volume': stage.volume,
        'volume_unit': stage.volume_unit,
    }

express_Stg = pluralized(express_stg)

class TestStageDataViewSet(ViewSetTest):
    Staging_Folder_Data.objects.all().delete()

    
    # list_url = lambda_fixture(lambda: '/stagingdata/')

    list_url = lambda_fixture(
        lambda:
            url_for('staging_folder_data-list'))

    detail_url = lambda_fixture(
        lambda staging_folder_data:
            url_for('staging_folder_data-detail', staging_folder_data.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        staging_folder_data = lambda_fixture(
            lambda: [
                Staging_Folder_Data.objects.create(
                    id=id,
                    customer=customer,
                    page=page,
                    brand=brand,
                    product=product,
                    discount_type=discount_type,
                    price_original=price_original,
                    price_with_discount=price_with_discount,
                    volume=volume,
                    volume_unit=volume_unit,
                )
                for (id, customer,page,brand,product,discount_type,price_original,price_with_discount,volume,volume_unit) in 
                [
                    (101, "customer1", 1,"brand1","product1","discount_type1",100,90,1,"volume_unit1"),
                    (102, "customer2", 2,"brand2","product2","discount_type2",101,91,2,"volume_unit2"),
                    (103, "customer3", 3,"brand3","product3","discount_type3",102,92,3,"volume_unit3")
                ]
            ],
            autouse=False,
        )
        
        def test_it_returns_values(self, staging_folder_data, json):
            expected = express_Stg(sorted(staging_folder_data, key=lambda stage: stage.id))
            actual = express_results(json['results'])
            assert expected == actual

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = static_fixture({
                    'customer':"customer1",
                    'page':4,
                    'brand':"brand",
                    'product':"xyz",
                    'discount_type':"discount_type4",
                    'price_original':104,
                    'price_with_discount':94,
                    'volume':4,
                    'volume_unit':"volume_unit4"
        })

        initial_stage_ids = precondition_fixture(
            lambda:
                set(Staging_Folder_Data.objects.values_list('id', flat=True)))
        
        def test_it_creates_new_stage(self, initial_stage_ids, json):
            json = express_result(json)
            expected = initial_stage_ids | {json['id']}
            actual = set(Staging_Folder_Data.objects.values_list('id', flat=True))
            assert expected == actual

        def test_it_sets_expected_attrs(self, data, json):
            json = express_result(json)
            stage = Staging_Folder_Data.objects.get(pk=json['id'])
            expected = data
            assert_model_attrs(stage, expected)

        def test_it_returns_stage(self, json):
            
            json = express_result(json)
            stage = Staging_Folder_Data.objects.get(pk=json['id'])
            expected = express_stg(stage)
            actual = json
            assert expected == actual


    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
    
        staging_folder_data = lambda_fixture(
            lambda:
                Staging_Folder_Data.objects.create(
                    customer="customer1",
                    page=4,
                    brand="brand",
                    product="xyz",
                    discount_type="test",
                    price_original=104,
                    price_with_discount=94,
                    volume=4,
                    volume_unit="volume_unit4"
                )
        )

        def test_it_returns_stage__(self, staging_folder_data, json):
            expected = express_stg(staging_folder_data)
            actual = express_result(json)
            assert expected == actual

    class TestUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        staging_folder_data = lambda_fixture(
            lambda:
                Staging_Folder_Data.objects.create(
                    
                    customer="customer1",
                    page=4,
                    brand="brand",
                    product="xyz",
                    discount_type="test",
                    price_original=104,
                    price_with_discount=94,
                    volume=4,
                    volume_unit="volume_unit4"
                ))

        data = static_fixture({

                    'customer':"customer1",
                    'page':4,
                    'brand':"brand",
                    'product':"xyz",
                    'discount_type':"test",
                    'price_original':104,
                    'price_with_discount':94,
                    'volume':4,
                    'volume_unit':"volume_unit4"
        })

        def test_it_sets_expected_attrs(self, data, staging_folder_data):
            # We must tell Django to grab fresh data from the database, or we'll
            # see our stale initial data and think our endpoint is broken!
            staging_folder_data.refresh_from_db()

            expected = data
            assert_model_attrs(staging_folder_data, expected)

        def test_it_returns_stage(self, staging_folder_data, json):
            staging_folder_data.refresh_from_db()

            expected = express_stg(staging_folder_data)
            print(expected)
            actual = express_result(json)
            print(actual)
            assert expected == actual

    class TestDestroy(
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns204,
    ):
        staging_folder_data = lambda_fixture(
            lambda:
                Staging_Folder_Data.objects.create(
                    customer="customer1",
                    page=4,
                    brand="brand",
                    product="xyz",
                    discount_type="test",
                    price_original=104,
                    price_with_discount=94,
                    volume=4,
                    volume_unit="volume_unit4"
                ))

        initial_stage_ids = precondition_fixture(
            lambda staging_folder_data:  # ensure our to-be-deleted Stores exists in our set
                set(Staging_Folder_Data.objects.values_list('id', flat=True)))

        def test_it_deletes_stage(self, initial_stage_ids, staging_folder_data):
            expected = initial_stage_ids - {staging_folder_data.id}
            actual = set(Staging_Folder_Data.objects.values_list('id', flat=True))
            assert expected == actual