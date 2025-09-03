from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'inventory', views.InventoryItemViewSet, basename='inventoryitem')
router.register(r'inventory-changes', views.InventoryChangeViewSet, basename='inventorychange')

urlpatterns = [
    path('', include(router.urls)),
]