from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user_register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user_login'),
    path('logout/', UserViewSet.as_view({'post': 'logout'}), name='user_logout'),
    path('profile/', UserViewSet.as_view({'get': 'profile', 'put': 'update_profile', 'patch': 'update_profile'}), name='user_profile'),
]