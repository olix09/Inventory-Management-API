from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from django.http import JsonResponse
from users.views import UserViewSet
from inventory.views import InventoryItemViewSet, InventoryChangeViewSet

def api_root(request):
    """API root endpoint with available endpoints"""
    return JsonResponse({
        'message': 'Welcome to Inventory Management API',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'users': '/api/users/',
            'inventory': '/api/inventory/',
            'inventory_changes': '/api/inventory-changes/',
            'admin': '/admin/',
        }
    })

# Create router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'inventory', InventoryItemViewSet)
router.register(r'inventory-changes', InventoryChangeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', obtain_auth_token, name='api_token_auth'),
    path('api/auth/', include('users.urls')),
    path('', api_root, name='api_root'),
]