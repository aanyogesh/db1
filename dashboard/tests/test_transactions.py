# tests/test_transaction.py
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
from dashboard.models import Transactions, Products, Stores, Customers

mock_product = Products.objects.create(
    name="Prod test name",
    ArticleFamily="ArticleFamily",
    ArticleSubfamily="ArticleSubfamily",
    ArticleCategory="ArticleCategory",
    active=True
)
mock_product1 = Products.objects.create(
    name="Prod test name1",
    ArticleFamily="ArticleFamily",
    ArticleSubfamily="ArticleSubfamily",
    ArticleCategory="ArticleCategory",
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
mock_store3 = Stores.objects.create(
    name="Mock store test name2",
    client_store_description="mock store test client_store_description1",
    email_id="mock@mail.com",
    contact_number="9090909090",
    address="test store address",
    active=True
)

mock_customer=Customers.objects.create(
    
    name="mock test Customer",
    email_id="mock@gmail.com",
    contact_number="9090909090",
    active=True,
    address="test Customer address"
)

mock_customer1=Customers.objects.create(
    
    name="mock test Customer1",
    email_id="mock@gmail.com",
    contact_number="9090909090",
    active=True,
    address="test Customer address"
)



Transaction_date = datetime.datetime.now()
Trans_date=Transaction_date.strftime("%Y-%m-%d")
def express_result(trans):
    return {
        'id': trans["id"],
        'customer': mock_customer.id,
        'store':mock_store1.id,
        'amount':trans["amount"],
        'price':trans["price"],
        'promotion':trans["promotion"],
        'transaction_date':Trans_date,
        'product':mock_product.id
    }
    
def express_results(results):
    res = [ express_result(trans) for trans in results ]
    return res

def express_trans(trans: Transactions) -> Dict[str, Any]:
    return {
        'id': trans.id,
        'customer': mock_customer.id,
        'store': mock_store1.id,
        'amount': trans.amount,
        'price': trans.price,
        'promotion': trans.promotion,
        'transaction_date': Trans_date,
        'product': mock_product.id
        
    }



express_trans = pluralized(express_trans)


def create_transcation(mock_store1,amount, price, promotion,transaction_date,mock_customer):
    
    trans_obj = Transactions.objects.create(
        customer = mock_customer,
        store = mock_store1,
        amount = amount,
        price = price,
        promotion=promotion,
        transaction_date = Trans_date,
        product = mock_product
        
    )
    return trans_obj

class TestTransDataViewSet(ViewSetTest):

    Transactions.objects.all().delete()
   
    
    list_url = lambda_fixture(
        lambda:
            url_for('transactions-list'))

    detail_url = lambda_fixture(
        lambda transactions:
            url_for('transactions-detail', transactions.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        transactions_obj = lambda_fixture(
            lambda: [
                create_transcation(store,amount, price, promotion,transaction_date,customer)
                for (store,amount, price, promotion,transaction_date,customer) in 
                [
                    ( mock_store1,100, 91,True,Trans_date,mock_customer),
                    ( mock_store2,101, 92,False,Trans_date,mock_customer1)
                    
                ]
            ],
            autouse=False,
        )

        # transactions_obj = lambda_fixture(
        #     lambda: [
        #         Transactions.objects.create(
        #             store=mock_store1,
        #             amount=amount,
        #             price=price,
        #             promotion=promotion,
        #             transaction_date=Trans_date,
        #             customer=mock_customer,
        #             product=mock_product                    
                    
        #         )
        #         for (store, amount, price, promotion, transaction_date,customer,product) in 
        #         [
        #             (mock_store1, 100,91,True,Trans_date,mock_customer,mock_product),
        #             (mock_store2, 101,92,False,Trans_date,mock_customer1,mock_product1)
        #         ]
        #     ],
        #     autouse=False,
        # )
        
        def test_it_returns_values(self, transactions_obj, results):
            #print("results:",results)
            expected = express_trans(sorted(transactions_obj, key=lambda trans: trans.id))
            actual = express_results(results)

            #print("expected:",expected)
            #print("**************"*5)
            #print("actual:",actual)

            assert expected == actual

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):

        mock_customer2=Customers.objects.create(
            
            name="mock test Customer2",
            email_id="mock@gmail.com",
            contact_number="9090909090",
            active=True,
            address="test Customer address"
        )
        data = static_fixture({
                    'store':mock_store2,
                    'amount':210,
                    'price':195,
                    'promotion':True,
                    'transaction_date':Trans_date,
                    'customer':mock_customer2
                    
                  })

        # initial_trans_ids = precondition_fixture(
        #     lambda:
        #         set(Transactions.objects.values_list('id', flat=True)))
        # def test_it_creates_new_trans(self, initial_trans_ids, json):
        #     print("json:",json)
        #     json = express_result(json)
        #     expected = initial_trans_ids | {json['id']}
        #     actual = set(Transactions.objects.values_list('id', flat=True))
        #     print("expected:",expected)
        #     print("**************"*5)
        #     print("actual:",actual)
        #     assert expected == actual

        def test_it_sets_expected_attrs(self, data, json):
            print("json:",json)
            json = express_result(json)
            trans = Transactions.objects.get(pk=json['id'])
            expected = data
            assert_model_attrs(trans, expected)

        def test_it_returns_trans(self, json):
            
            json = express_result(json)
            trans = Transactions.objects.get(pk=json['id'])
            expected = express_trans(trans)
            actual = json
            assert expected == actual


    # class TestRetrieve(
    #     UsesGetMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    
    #     transactions = lambda_fixture(
    #         lambda:
    #             Transactions.objects.create(
    #                 'amount':100,
    #                 'price':91,
    #                 'promotion':True
    #             )
    #     )

    #     def test_it_returns_trans__(self, transactions, json):
    #         expected = express_trans(transactions)
    #         actual = express_result(json)
    #         assert expected == actual

    # class TestUpdate(
    #     UsesPatchMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    #     transactions = lambda_fixture(
    #         lambda:
    #             Transactions.objects.create(
    #                 amount = 100,
    #                 price = 91,
    #                 promotion = True
    #             ))

    #     data = static_fixture({
    #                 'amount':"100",
    #                 'price':91,
    #                 'promotion':True
    #                 
    #     })

    #     def test_it_sets_expected_attrs(self, data, transactions):
    #         # We must tell Django to grab fresh data from the database, or we'll
    #         # see our stale initial data and think our endpoint is broken!
    #         transactions.refresh_from_db()

    #         expected = data
    #         assert_model_attrs(transactions, expected)

    #     def test_it_returns_trans(self, transactions, json):
    #         transactions.refresh_from_db()

    #         expected = express_trans(transactions)
    #         print(expected)
    #         actual = express_result(json)
    #         print(actual)
    #         assert expected == actual

    # class TestDestroy(
    #     UsesDeleteMethod,
    #     UsesDetailEndpoint,
    #     Returns204,
    # ):
    #     transactions = lambda_fixture(
    #         lambda:
    #             Transactions.objects.create(
    #                 amount = 100,
    #                 price = 91,
    #                 promotion = True
    #             ))

    #     initial_trans_ids = precondition_fixture(
    #         lambda transactions:  # ensure our to-be-deleted Stores exists in our set
    #             set(Transactions.objects.values_list('id', flat=True)))

    #     def test_it_deletes_trans(self, initial_trans_ids, transactions):
    #         expected = initial_trans_ids - {transactions.id}
    #         actual = set(Transactions.objects.values_list('id', flat=True))
    #         assert expected == actual