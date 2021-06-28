# from typing import Any, Dict
# from django.conf import settings
# settings.configure()
# import django
# django.setup()
# from pytest_common_subject import precondition_fixture
# from pytest_drf import (
#     ViewSetTest,
#     Returns200,
#     Returns201,
#     Returns204,
#     UsesGetMethod,
#     UsesDeleteMethod,
#     UsesDetailEndpoint,
#     UsesListEndpoint,
#     UsesPatchMethod,
#     UsesPostMethod,
# )
# from pytest_drf.util import pluralized, url_for
# from pytest_lambda import lambda_fixture, static_fixture
# from pytest_assert_utils import assert_model_attrs

# from dashboard.views import ProductsViewSet as KeyValue


# def express_key_value(kv: KeyValue) -> Dict[str, Any]:
#     return {
#         'id': kv.id,
#         'name': kv.name,
#         'ArticleFamily': kv.ArticleFamily
#     }

# express_key_values = pluralized(express_key_value)


# class TestKeyValueViewSet(ViewSetTest):
#     list_url = lambda_fixture(
#         lambda:
#             url_for('dashboard-products'))

#     detail_url = lambda_fixture(
#         lambda key_value:
#             url_for('product-detail', key_value.pk))

#     class TestList(
#         UsesGetMethod,
#         UsesListEndpoint,
#         Returns200,
#     ):
#         key_values = lambda_fixture(
#             lambda: [
#                 KeyValue.objects.create(key=key, value=value)
#                 for key, value in {
#                     'name1': 'ArticleFamily1',
#                     'name2': 'ArticleFamily2',
#                     'name3': 'ArticleFamily3',
#                 }.items()
#             ],
#             autouse=True,
#         )

#         def test_it_returns_key_values(self, key_values, results):
#             expected = express_key_values(sorted(key_values, key=lambda kv: kv.id))
#             actual = results
#             assert expected == actual

#     # class TestCreate(
#     #     UsesPostMethod,
#     #     UsesListEndpoint,
#     #     Returns201,
#     # ):
#     #     data = static_fixture({
#     #         'key': 'snakes',
#     #         'value': 'hissssssss',
#     #     })

#     #     initial_key_value_ids = precondition_fixture(
#     #         lambda:
#     #             set(KeyValue.objects.values_list('id', flat=True)))

#     #     def test_it_creates_new_key_value(self, initial_key_value_ids, json):
#     #         expected = initial_key_value_ids | {json['id']}
#     #         actual = set(KeyValue.objects.values_list('id', flat=True))
#     #         assert expected == actual

#     #     def test_it_sets_expected_attrs(self, data, json):
#     #         key_value = KeyValue.objects.get(pk=json['id'])

#     #         expected = data
#     #         assert_model_attrs(key_value, expected)

#     #     def test_it_returns_key_value(self, json):
#     #         key_value = KeyValue.objects.get(pk=json['id'])

#     #         expected = express_key_value(key_value)
#     #         actual = json
#     #         assert expected == actual


#     # class TestRetrieve(
#     #     UsesGetMethod,
#     #     UsesDetailEndpoint,
#     #     Returns200,
#     # ):
#     #     key_value = lambda_fixture(
#     #         lambda:
#     #             KeyValue.objects.create(
#     #                 key='monty',
#     #                 value='jython',
#     #             ))

#     #     def test_it_returns_key_value(self, key_value, json):
#     #         expected = express_key_value(key_value)
#     #         actual = json
#     #         assert expected == actual

#     # class TestUpdate(
#     #     UsesPatchMethod,
#     #     UsesDetailEndpoint,
#     #     Returns200,
#     # ):
#     #     key_value = lambda_fixture(
#     #         lambda:
#     #             KeyValue.objects.create(
#     #                 key='pipenv',
#     #                 value='was a huge leap forward',
#     #             ))

#     #     data = static_fixture({
#     #         'key': 'buuut poetry',
#     #         'value': 'locks quicker and i like that',
#     #     })

#     #     def test_it_sets_expected_attrs(self, data, key_value):
#     #         # We must tell Django to grab fresh data from the database, or we'll
#     #         # see our stale initial data and think our endpoint is broken!
#     #         key_value.refresh_from_db()

#     #         expected = data
#     #         assert_model_attrs(key_value, expected)

#     #     def test_it_returns_key_value(self, key_value, json):
#     #         key_value.refresh_from_db()

#     #         expected = express_key_value(key_value)
#     #         actual = json
#     #         assert expected == actual

#     # class TestDestroy(
#     #     UsesDeleteMethod,
#     #     UsesDetailEndpoint,
#     #     Returns204,
#     # ):
#     #     key_value = lambda_fixture(
#     #         lambda:
#     #             KeyValue.objects.create(
#     #                 key='i love',
#     #                 value='YOU',
#     #             ))

#     #     initial_key_value_ids = precondition_fixture(
#     #         lambda key_value:  # ensure our to-be-deleted KeyValue exists in our set
#     #             set(KeyValue.objects.values_list('id', flat=True)))

#     #     def test_it_deletes_key_value(self, initial_key_value_ids, key_value):
#     #         expected = initial_key_value_ids - {key_value.id}
#     #         actual = set(KeyValue.objects.values_list('id', flat=True))
#     #         assert expected == actual