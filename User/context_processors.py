from django.conf import settings

def firebase_config(request):
    return {
        'firebase_config': getattr(settings, 'FIREBASE_CONFIG', {}),
        'user_id': request.user.id if request.user.is_authenticated else None,
    }