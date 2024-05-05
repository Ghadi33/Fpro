from django.contrib.auth.models import AnonymousUser
from .models import UserProfile

def profile_data(request):
    profile = None
    if request.user.is_authenticated and not isinstance(request.user, AnonymousUser):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return {'user_profile': profile}
