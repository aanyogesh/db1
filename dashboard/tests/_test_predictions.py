# tests/test_Predictions.py
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
from dashboard.models import Products, Predictions, Stores, CompositeKey, Customers, User

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

mock_store = Stores.objects.create(
    name="Mock store test name",
    client_store_description="mock store test client_store_description",
    email_id="mock@mail.com",
    contact_number="9090909090",
    address="test store address",
    active=True
)
mock_store1 = Stores.objects.create(
    name="Mock store test name1",
    client_store_description="mock store test client_store_description",
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
mock_user=User.objects.create(
    username="name1",
    
)


mock_compositekey=CompositeKey.objects.create(
    customer=mock_customer,
    product=mock_product,
    store=mock_store,
    client=mock_user
    
)

tsnow = datetime.datetime.now()
Tsnow=tsnow.strftime("%Y-%m-%d")

tsforecast=datetime.datetime.now()
Tsforecast=tsforecast.strftime("%Y-%m-%d")

prediction_date=datetime.datetime.now()
Prediction_date=prediction_date.strftime("%Y-%m-%d")
def express_result(predi):
    return {
        'id': predi["id"],
        'customer': mock_customer.id,
        'product': mock_product.id,
        'store': mock_store.id,
        'compositeKey': mock_compositekey.id,
        'tsnow': Tsnow,
        'tsforecast': Tsforecast,
        'prediction_value': predi["prediction_value"],
        'prediction_date': predi["prediction_date"],
        'prediction_valid_date': predi["prediction_valid_date"],
        'model': predi["model"],
        'experiment': predi["experiment"]
    }
    
def express_results(results):
    res = [ express_result(predi) for predi in results ]
    return res

def express_predictions(predi: Predictions) -> Dict[str, Any]:
    return {
        'id': predi.id,
        'customer': mock_customer.id,
        'product': mock_product.id,
        'store': mock_store.id,
        'compositeKey':  mock_compositekey.id,
        'tsnow': Tsnow,
        'tsforecast': Tsforecast,
        'prediction_value': predi.prediction_value,
        'prediction_date': predi.prediction_date,
        'prediction_valid_date': predi.prediction_valid_date,
        'model': predi.model,
        'experiment': predi.experiment
    }

express_predictions = pluralized(express_predictions)

# def create_prediction(prediction_value, model, experiment):
#     predictions_obj = Predictions.objects.create(

#         prediction_value=prediction_value,
#         model=model,
#         experiment=experiment,
#         customer=mock_customer,
#         product=mock_product,
#         store=mock_store,
#         compositeKey=mock_compositekey
#     )
#     return predictions_obj


class TestPredictionViewSet(ViewSetTest):
    Predictions.objects.all().delete()

    list_url = lambda_fixture(
        lambda:
            url_for('predictions-list'))

    detail_url = lambda_fixture(
        lambda predictions:
            url_for('predictions-detail', predictions.id))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):

        
        # predictions_objs = lambda_fixture(
        #     lambda: [
        #         create_prediction(prediction_value, model, experiment)
        #         for (prediction_value, model, experiment) in 
        #         [
        #             (100, "model1","experiment1"),
        #             (101, "model2","experiment2")
                    
        #         ]
        #     ],
        #     autouse=False,
        # )
        predictions_objs = lambda_fixture(
            lambda: [
                Predictions.objects.create(
                    prediction_value=prediction_value,
                    model=model,
                    experiment=experiment,
                    customer=mock_customer,
                    product=mock_product,
                    store=mock_store,
                    tsnow=Tsnow,
                    tsforecast=Tsforecast,
                    prediction_date=Prediction_date,
                    compositeKey=mock_compositekey
                    
                )
                for (prediction_value, model, experiment, customer, product,store,tsnow,tsforecast,prediction_date,compositeKey) in 
                [
                    (100, "model1","experiment1",mock_customer,mock_product,mock_store,tsnow,Tsforecast,Prediction_date,mock_compositekey),
                    (101, "model2","experiment2",mock_customer1,mock_product1,mock_store1,tsnow,Tsforecast,Prediction_date,mock_compositekey)
                ]
            ],
            autouse=False,
        )

        
        def test_it_returns_values(self, predictions_objs, results):
            expected = express_predictions(sorted(predictions_objs, key=lambda predi: predi.id))
            actual = express_results(results)
            assert expected == actual

    # class TestCreate(
    #     UsesPostMethod,
    #     UsesListEndpoint,
    #     Returns201,
    # ):
    #     data = static_fixture({
    #         'prediction_value': 100,
    #         'model': "model1",
    #         'experiment': "experiment1"
            
    #     })

    #     initial_prediction_ids = precondition_fixture(
    #         lambda:
    #             set(Predictions.objects.values_list('id', flat=True)))

    #     def test_it_creates_new_predictions(self, initial_prediction_ids, json):
    #         json = express_result(json)
    #         expected = initial_prediction_ids | {json['id']}
    #         actual = set(Predictions.objects.values_list('id', flat=True))
    #         assert expected == actual

    #     def test_it_sets_expected_attrs(self, data, json):
    #         json = express_result(json)
    #         predictions = Predictions.objects.get(pk=json['id'])
    #         expected = data
    #         assert_model_attrs(predictions, expected)

    #     def test_it_returns_predictions(self, json):
    #         json = express_result(json)
    #         predictions = Predictions.objects.get(pk=json['id'])

    #         expected = express_predictions(predictions)
    #         actual = json
    #         assert expected == actual


    # class TestRetrieve(
    #     UsesGetMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    #     predictions = lambda_fixture(
    #         lambda:
    #             Predictions.objects.create(
    #                 prediction_value= 100,
    #                 model= "model1",
    #                 experiment= "experiment1"

    #             ))

    #     def test_it_returns_predictions(self, predictions, json):
    #         expected = express_predictions(predictions)
    #         actual = express_result(json)
    #         assert expected == actual

    # class TestUpdate(
    #     UsesPatchMethod,
    #     UsesDetailEndpoint,
    #     Returns200,
    # ):
    #     predictions = lambda_fixture(
    #         lambda:
    #             Predictions.objects.create(
    #                 prediction_value= 100,
    #                 model= "model1",
    #                 experiment= "experiment1"

    #             ))

    #     data = static_fixture({
    #         'prediction_value': 100,
    #         'model': "model1",
    #         'experiment': "experiment1"
            
    #     })

    #     def test_it_sets_expected_attrs(self, data, predictions):
    #         Predictions.refresh_from_db()
    #         expected = data
    #         assert_model_attrs(predictions, expected)

    #     def test_it_returns_predictions(self, predictions, json):
    #         Predictions.refresh_from_db()
    #         expected = express_predictions(predictions)
    #         actual = express_result(json)
    #         assert expected == actual

    # class TestDestroy(
    #     UsesDeleteMethod,
    #     UsesDetailEndpoint,
    #     Returns204,
    # ):
    #     predictions = lambda_fixture(
    #         lambda:
    #             Predictions.objects.create(

    #                 prediction_value= 100,
    #                 model= "model1",
    #                 experiment= "experiment1"
                    
    #             ))

    #     initial_predictions_ids = precondition_fixture(
    #         lambda predictions:  
    #             set(Predictions.objects.values_list('id', flat=True)))

    #     def test_it_deletes_predictions(self, initial_predictions_ids, predictions):
    #         expected = initial_predictions_ids - {predictions.id}
    #         actual = set(Predictions.objects.values_list('id', flat=True))
    #         assert expected == actual