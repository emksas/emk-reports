from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import IncomeViewSet

router = DefaultRouter()
# Automatically registers the IncomeViewSet CRUD routes under /api/incomes/.
router.register(r'incomes', IncomeViewSet, basename='income')

# Also accepts requests without a trailing slash, such as /api/incomes.
no_slash_router = SimpleRouter(trailing_slash=False)
no_slash_router.register(r'incomes', IncomeViewSet, basename='income-no-slash')

urlpatterns = router.urls + no_slash_router.urls
