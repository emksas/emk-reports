from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from rest_framework import status

from apps.incomes.models import Income
from apps.incomes.serializers import IncomeSerializer
from apps.incomes.views import IncomeViewSet


class IncomeSerializerTests(SimpleTestCase):
    def test_serializer_exposes_all_income_fields(self):
        serializer = IncomeSerializer()

        self.assertEqual(
            set(serializer.fields.keys()),
            {
                "id",
                "value",
                "source",
                "category",
                "payment_method",
                "date",
                "reference",
                "financial_planning_id",
                "accounting_account_id",
                "user_id",
            },
        )


class IncomeViewSetTests(SimpleTestCase):
    def setUp(self):
        self.viewset = IncomeViewSet()
        self.print_patcher = patch("builtins.print")
        self.print_patcher.start()
        self.addCleanup(self.print_patcher.stop)

    @patch("apps.incomes.views.Income.objects")
    def test_get_queryset_filters_by_user_and_account(self, income_objects):
        base_queryset = Mock()
        user_queryset = Mock()
        account_queryset = Mock()
        income_objects.all.return_value = base_queryset
        base_queryset.filter.return_value = user_queryset
        user_queryset.filter.return_value = account_queryset
        self.viewset.request = SimpleNamespace(
            query_params={"user_id": "7", "account_id": "3"}
        )

        result = self.viewset.get_queryset()

        income_objects.all.assert_called_once_with()
        base_queryset.filter.assert_called_once_with(user_id="7")
        user_queryset.filter.assert_called_once_with(accounting_account_id="3")
        self.assertIs(result, account_queryset)

    @patch("apps.incomes.views.Income.objects")
    def test_get_queryset_returns_all_when_filters_are_missing(self, income_objects):
        queryset = Mock()
        income_objects.all.return_value = queryset
        self.viewset.request = SimpleNamespace(query_params={})

        result = self.viewset.get_queryset()

        income_objects.all.assert_called_once_with()
        queryset.filter.assert_not_called()
        self.assertIs(result, queryset)

    def test_list_returns_serialized_queryset(self):
        request = SimpleNamespace()
        queryset = [Mock(spec=Income)]
        serializer = Mock(data=[{"id": 1, "value": "100.00"}])
        self.viewset.get_queryset = Mock(return_value=queryset)
        self.viewset.get_serializer = Mock(return_value=serializer)

        response = self.viewset.list(request)

        self.viewset.get_serializer.assert_called_once_with(queryset, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_returns_created_when_payload_is_valid(self):
        request = SimpleNamespace(data={"value": "250.00", "user_id": 9})
        serializer = Mock(data={"id": 4, "value": "250.00"})
        serializer.is_valid.return_value = True
        self.viewset.get_serializer = Mock(return_value=serializer)

        response = self.viewset.create(request)

        self.viewset.get_serializer.assert_called_once_with(data=request.data)
        serializer.is_valid.assert_called_once_with()
        serializer.save.assert_called_once_with()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_create_returns_bad_request_when_payload_is_invalid(self):
        request = SimpleNamespace(data={"user_id": 9})
        serializer = Mock(errors={"value": ["This field is required."]})
        serializer.is_valid.return_value = False
        self.viewset.get_serializer = Mock(return_value=serializer)

        response = self.viewset.create(request)

        serializer.save.assert_not_called()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)

    @patch("apps.incomes.views.Income.objects")
    def test_update_by_user_account_updates_matching_income(self, income_objects):
        request = SimpleNamespace(
            data={
                "user_id": 2,
                "account_id": 8,
                "value": "900.00",
                "accounting_account_id": 8,
            }
        )
        income = Mock(spec=Income)
        serializer = Mock(data={"id": 5, "value": "900.00"})
        serializer.is_valid.return_value = True
        income_objects.get.return_value = income
        self.viewset.get_serializer = Mock(return_value=serializer)

        response = self.viewset.update_by_user_account(request)

        income_objects.get.assert_called_once_with(user_id=2, accounting_account_id=8)
        self.viewset.get_serializer.assert_called_once_with(income, data=request.data)
        serializer.save.assert_called_once_with()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    @patch("apps.incomes.views.Income.objects")
    def test_update_by_user_account_returns_not_found_when_income_is_missing(
        self, income_objects
    ):
        request = SimpleNamespace(data={"user_id": 2, "account_id": 8})
        income_objects.get.side_effect = Income.DoesNotExist

        response = self.viewset.update_by_user_account(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "No encontrado"})

    @patch("apps.incomes.views.Income.objects")
    def test_delete_by_user_account_deletes_matching_income(self, income_objects):
        request = SimpleNamespace(query_params={"user_id": "2", "account_id": "8"})
        income = Mock(spec=Income)
        income_objects.get.return_value = income

        response = self.viewset.delete_by_user_account(request)

        income_objects.get.assert_called_once_with(user_id="2", accounting_account_id="8")
        income.delete.assert_called_once_with()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch("apps.incomes.views.Income.objects")
    def test_delete_by_user_account_returns_not_found_when_income_is_missing(
        self, income_objects
    ):
        request = SimpleNamespace(query_params={"user_id": "2", "account_id": "8"})
        income_objects.get.side_effect = Income.DoesNotExist

        response = self.viewset.delete_by_user_account(request)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "No encontrado"})
