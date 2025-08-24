from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import CustomUser
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users with registration and profile management
    """
    # Explicit queryset is now defined (fix for router error)
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Different permissions for different actions
        """
        if self.action in ['create', 'register']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """Users can only view their own profile unless admin"""
        if self.request.user.is_staff:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """Login user and return token"""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Login successful'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """Logout user and delete token"""
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'message': 'No active session found'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'user': serializer.data,
                'message': 'Profile updated successfully'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
