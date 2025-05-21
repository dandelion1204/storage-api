from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product import views

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('ingredients', views.IngredientViewSet)
router.register('ingredientlots', views.IngredientLotViewSet)

app_name = 'product'

urlpatterns = [
    path('', include(router.urls)),
]