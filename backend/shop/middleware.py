import firebase_admin
from firebase_admin import auth, credentials
from django.conf import settings
from django.http import JsonResponse
import json

# Initialize Firebase Admin SDK
if settings.GOOGLE_APPLICATION_CREDENTIALS and not firebase_admin._apps:
    try:
        cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase initialization error: {e}")

class FirebaseAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip authentication for certain paths
        skip_paths = [
            '/api/categories/',
            '/api/products/',
            '/api/contact/',
            '/admin/',
        ]
        
        if any(request.path.startswith(path) for path in skip_paths):
            return self.get_response(request)

        # Check for Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
            try:
                # Verify Firebase token
                decoded_token = auth.verify_id_token(token)
                request.user = {
                    'uid': decoded_token['uid'],
                    'email': decoded_token.get('email', ''),
                    'authenticated': True
                }
            except Exception as e:
                # For development, allow placeholder tokens
                if settings.DEBUG and token == 'firebase-token-placeholder':
                    request.user = {
                        'uid': 'dev-user-123',
                        'email': 'dev@example.com',
                        'authenticated': True
                    }
                else:
                    return JsonResponse({'error': 'Invalid token'}, status=401)
        else:
            request.user = {'authenticated': False}

        return self.get_response(request)