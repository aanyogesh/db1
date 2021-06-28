# tests/test_store.py
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
from dashboard.models import Stores

def express_result(stor):
    return {
        'id': stor["id"],
        'name': stor["name"],
        'email_id': stor["email_id"],
        'contact_number': stor["contact_number"],
        'address': stor["address"],
        'active': stor["active"],
    }
    
def express_results(results):
    res = [ express_result(stor) for stor in results ]
    return res

def express_store(stor: Stores) -> Dict[str, Any]:
    return {
        'id': stor.id,
        'name': stor.name,
        'email_id': stor.email_id,
        'contact_number': stor.contact_number,
        'address': stor.address,
        'active': stor.active,
    }

express_Stores = pluralized(express_store)

class TestStoresViewSet(ViewSetTest):
    Stores.objects.all().delete()

    list_url = lambda_fixture(
        lambda:
            url_for('stores-list'))

    detail_url = lambda_fixture(
        lambda store:
            url_for('stores-detail', store.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        Stores = lambda_fixture(
            lambda: [
                Stores.objects.create(
                    name=name,
                    email_id=email_id,
                    contact_number=contact_number,
                    address=address,
                    active=active
                )
                for (name, email_id, contact_number, address, active) in 
                [
                    ("name11", "email_id1", "7896523652", "address1", True),
                    ("name22", "email_id2", "7412589632", "address2", False),
                    ("name33", "email_id3", "1452369857", "address3", False)
                ]
            ],
            autouse=False,
        )
        
        def test_it_returns_values(self, Stores, results):
            print("json:",results)
            expected = express_Stores(sorted(Stores, key=lambda stor: stor.id))
            print("expected:", expected)
            print("json:",results)
            actual = express_results(results)
            assert expected == actual

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = static_fixture({
            'name': "name4",
            'email_id': "email_id4",
            'contact_number': "7458963254",
            'address': "address4",
            'active': True,
        })

        initial_store_ids = precondition_fixture(
            lambda:
                set(Stores.objects.values_list('id', flat=True)))

        def test_it_creates_new_store(self, initial_store_ids, json):
            json = express_result(json)
            expected = initial_store_ids | {json['id']}
            actual = set(Stores.objects.values_list('id', flat=True))
            assert expected == actual

        def test_it_sets_expected_attrs(self, data, json):
            json = express_result(json)
            store = Stores.objects.get(pk=json['id'])
            expected = data
            assert_model_attrs(store, expected)

        def test_it_returns_store(self, json):
            json = express_result(json)
            store = Stores.objects.get(pk=json['id'])

            expected = express_store(store)
            actual = json
            assert expected == actual


    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        store = lambda_fixture(
            lambda:
                Stores.objects.create(
                    name="name4",
                    email_id="email_id4",
                    contact_number="contact_number4",
                    address="address4",
                    active=True
                ))

        def test_it_returns_store(self, store, json):
            expected = express_store(store)
            actual = express_result(json)
            assert expected == actual

    class TestUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        store = lambda_fixture(
            lambda:
                Stores.objects.create(
                    name="name4",
                    email_id="email_id4",
                    contact_number="7896541258",
                    address="address4",
                    active=True
                ))

        data = static_fixture({
            'name': "name4",
            'email_id': "email_id4",
            'contact_number': "7896541258",
            'address': "address4",
            'active': True,
        })

        def test_it_sets_expected_attrs(self, data, store):
            # We must tell Django to grab fresh data from the database, or we'll
            # see our stale initial data and think our endpoint is broken!
            store.refresh_from_db()

            expected = data
            assert_model_attrs(store, expected)

        def test_it_returns_store(self, store, json):
            store.refresh_from_db()

            expected = express_store(store)
            actual = express_result(json)
            assert expected == actual

    class TestDestroy(
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns204,
    ):
        store = lambda_fixture(
            lambda:
                Stores.objects.create(
                    name="name4",
                    email_id="email_id4",
                    contact_number="7412589632",
                    address="address4",
                    active=True
                ))

        initial_store_ids = precondition_fixture(
            lambda store:  # ensure our to-be-deleted Stores exists in our set
                set(Stores.objects.values_list('id', flat=True)))

        def test_it_deletes_store(self, initial_store_ids, store):
            expected = initial_store_ids - {store.id}
            actual = set(Stores.objects.values_list('id', flat=True))
            assert expected == actual