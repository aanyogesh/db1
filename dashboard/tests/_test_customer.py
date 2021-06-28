# tests/test_customer.py
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
from dashboard.models import Customers

def express_result(cust):
    return {
        'id': cust["id"],
        'name': cust["name"],
        'email_id': cust["email_id"],
        'contact_number': cust["contact_number"],
        'address': cust["address"],
        'active': cust["active"],
    }
    
def express_results(results):
    res = [ express_result(cust) for cust in results ]
    return res

def express_customer(cust: Customers) -> Dict[str, Any]:
    return {
        'id': cust.id,
        'name': cust.name,
        'email_id': cust.email_id,
        'contact_number': cust.contact_number,
        'address': cust.address,
        'active': cust.active,
    }

express_Customers = pluralized(express_customer)

class TestCustomersViewSet(ViewSetTest):
    Customers.objects.all().delete()

    list_url = lambda_fixture(
        lambda:
            url_for('customers-list'))

    detail_url = lambda_fixture(
        lambda customer:
            url_for('customers-detail', customer.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        Customers = lambda_fixture(
            lambda: [
                Customers.objects.create(
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
        
        def test_it_returns_values(self, Customers, results):
            print("json:",results)
            expected = express_Customers(sorted(Customers, key=lambda cust: cust.id))
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

        initial_customer_ids = precondition_fixture(
            lambda:
                set(Customers.objects.values_list('id', flat=True)))

        def test_it_creates_new_customer(self, initial_customer_ids, json):
            json = express_result(json)
            expected = initial_customer_ids | {json['id']}
            actual = set(Customers.objects.values_list('id', flat=True))
            assert expected == actual

        def test_it_sets_expected_attrs(self, data, json):
            json = express_result(json)
            customer = Customers.objects.get(pk=json['id'])
            expected = data
            assert_model_attrs(customer, expected)

        def test_it_returns_customer(self, json):
            json = express_result(json)
            customer = Customers.objects.get(pk=json['id'])

            expected = express_customer(customer)
            actual = json
            assert expected == actual


    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        customer = lambda_fixture(
            lambda:
                Customers.objects.create(
                    name="name4",
                    email_id="email_id4",
                    contact_number="contact_number4",
                    address="address4",
                    active=True
                ))

        def test_it_returns_customer(self, customer, json):
            expected = express_customer(customer)
            actual = express_result(json)
            assert expected == actual

    class TestUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        customer = lambda_fixture(
            lambda:
                Customers.objects.create(
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

        def test_it_sets_expected_attrs(self, data, customer):
            # We must tell Django to grab fresh data from the database, or we'll
            # see our stale initial data and think our endpoint is broken!
            customer.refresh_from_db()

            expected = data
            assert_model_attrs(customer, expected)

        def test_it_returns_customer(self, customer, json):
            customer.refresh_from_db()

            expected = express_customer(customer)
            actual = express_result(json)
            assert expected == actual

    class TestDestroy(
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns204,
    ):
        customer = lambda_fixture(
            lambda:
                Customers.objects.create(
                    name="name4",
                    email_id="email_id4",
                    contact_number="7412589632",
                    address="address4",
                    active=True
                ))

        initial_customer_ids = precondition_fixture(
            lambda customer:  # ensure our to-be-deleted Customers exists in our set
                set(Customers.objects.values_list('id', flat=True)))

        def test_it_deletes_customer(self, initial_customer_ids, customer):
            expected = initial_customer_ids - {customer.id}
            actual = set(Customers.objects.values_list('id', flat=True))
            assert expected == actual