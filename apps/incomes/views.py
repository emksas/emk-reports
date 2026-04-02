from rest_framework import viewsets
from .models import Income
from .serializers import IncomeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

class IncomeViewSet( viewsets.ModelViewSet ):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def  get_queryset(self):
        queryset = Income.objects.all()

        userId = self.request.query_params.get('user_id')
        accountId =  self.request.query_params.get('account_id')

        if userId:
            queryset = queryset.filter(user_id=userId)

        if accountId:
            queryset = queryset.filter(accounting_account_id=accountId)

        print( queryset )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.queryset()

        if not queryset.exists():
            return Response(
                {"message": "there is no results"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='update-by-user-account')
    def update_by_user_account(self, request):
        user_id = request.data.get('user_id')
        account_id = request.data.get('account_id')

        try:
            income = Income.objects.get(
                user_id=user_id,
                accounting_account_id=account_id
            )
        except Income.DoesNotExist:
            return Response({"error": "No encontrado"}, status=404)

        serializer = self.get_serializer(income, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=['delete'], url_path='delete-by-user-account')
    def delete_by_user_account(self, request):
        user_id = request.query_params.get('user_id')
        account_id = request.query_params.get('account_id')

        try:
            income = Income.objects.get(
                user_id=user_id,
                accounting_account_id=account_id
            )
        except Income.DoesNotExist:
            return Response({"error": "No encontrado"}, status=404)

        income.delete()
        return Response(status=204)