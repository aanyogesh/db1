# tests/test_promotion.py
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
from dashboard.models import Promotion

def express_result(prom):
    return {
        'id': prom["id"],
        'name': prom["name"],
        'promotion_description': prom["promotion_description"],
        'active': prom["active"],
    }
    
def express_results(results):
    res = [ express_result(prom) for prom in results ]
    return res

def express_promotion(prom: Promotion) -> Dict[str, Any]:
    return {
        'id': prom.id,
        'name': prom.name,
        'promotion_description': prom.promotion_description,
        'active': prom.active,
    }

express_Promotion = pluralized(express_promotion)

class TestPromotionViewSet(ViewSetTest):
    Promotion.objects.all().delete()

    list_url = lambda_fixture(
        lambda:
            url_for('promotion-list'))

    detail_url = lambda_fixture(
        lambda promotion:
            url_for('promotion-detail', promotion.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        Promotion = lambda_fixture(
            lambda: [
                Promotion.objects.create(
                    name=name,
                    promotion_description=promotion_description,
                    active=active
                )
                for (name, promotion_description, active) in 
                [
                    ("name11", "promotion_description1", True),
                    ("name22", "promotion_description2",  False),
                    ("name33", "promotion_description3", False)
                ]
            ],
            autouse=False,
        )
        
        # def test_it_returns_values(self, Promotion, results):
        #     print("json:",results)
        #     expected = express_Promotion(sorted(Promotion, key=lambda prom: prom.id))
        #     print("expected:", expected)
        #     print("json:",results)
        #     actual = express_results(results)
        #     assert expected == actual

    # class TestCreate(
    #     UsesPostMethod,
    #     UsesListEndpoint,
    #     Returns201,
    # ):
    #     data = static_fixture({
    #         'name': "name4",
    #         'promotion_description': "promotion_description4",
    #         'store': "7458963254",
    #         'address': "address4",
    #         'active': True,
    #     })

    #     initial_promotion_ids = precondition_fixture(
    #         lambda:
    #             set(Promotion.objects.values_list('id', flat=True)))

    #     def test_it_creates_new_promotion(self, initial_promotion_ids, json):
    #         json = express_result(json)
    #         expected = initial_promotion_ids | {json['id']}
    #         actual = set(Promotion.objects.values_list('id', flat=True))
    #         assert expected == actual

    #     def test_it_sets_expected_attrs(self, data, json):
    #         json = express_result(json)
    #         promotion = Promotion.objects.get(pk=json['id'])
    #         expected = data
    #         assert_model_attrs(promotion, expected)

    #     def test_it_returns_promotion(self, json):
    #         json = express_result(json)
    #         promotion = Promotion.objects.get(pk=json['id'])

    #         expected = express_promotion(promotion)
    #         actual = json
    #         assert expected == actual


    # class TestRetrieve(
    #     UsesGetMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    #     promotion = lambda_fixture(
    #         lambda:
    #             Promotion.objects.create(
    #                 name="name4",
    #                 promotion_description="promotion_description4",
    #                 store="store4",
    #                 address="address4",
    #                 active=True
    #             ))

    #     def test_it_returns_promotion(self, promotion, json):
    #         expected = express_promotion(promotion)
    #         actual = express_result(json)
    #         assert expected == actual

    # class TestUpdate(
    #     UsesPatchMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    #     promotion = lambda_fixture(
    #         lambda:
    #             Promotion.objects.create(
    #                 name="name4",
    #                 promotion_description="promotion_description4",
    #                 store="7896541258",
    #                 address="address4",
    #                 active=True
    #             ))

    #     data = static_fixture({
    #         'name': "name4",
    #         'promotion_description': "promotion_description4",
    #         'store': "7896541258",
    #         'address': "address4",
    #         'active': True,
    #     })

    #     def test_it_sets_expected_attrs(self, data, promotion):
    #         # We must tell Django to grab fresh data from the database, or we'll
    #         # see our stale initial data and think our endpoint is broken!
    #         promotion.refresh_from_db()

    #         expected = data
    #         assert_model_attrs(promotion, expected)

    #     def test_it_returns_promotion(self, promotion, json):
    #         promotion.refresh_from_db()

    #         expected = express_promotion(promotion)
    #         actual = express_result(json)
    #         assert expected == actual

    # class TestDestroy(
    #     UsesDeleteMethod,
    #     UsesDetailEndpoint,
    #     Returns204,
    # ):
    #     promotion = lambda_fixture(
    #         lambda:
    #             Promotion.objects.create(
    #                 name="name4",
    #                 promotion_description="promotion_description4",
    #                 store="7412589632",
    #                 address="address4",
    #                 active=True
    #             ))

    #     initial_promotion_ids = precondition_fixture(
    #         lambda promotion:  # ensure our to-be-deleted Promotion exists in our set
    #             set(Promotion.objects.values_list('id', flat=True)))

    #     def test_it_deletes_promotion(self, initial_promotion_ids, promotion):
    #         expected = initial_promotion_ids - {promotion.id}
    #         actual = set(Promotion.objects.values_list('id', flat=True))
    #         assert expected == actual