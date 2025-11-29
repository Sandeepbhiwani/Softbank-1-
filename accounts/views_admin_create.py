from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

def create_admin(request):
    secret = request.GET.get("key")

    if secret != "akm12345":  # apna secret key
        return HttpResponse("Unauthorized", status=403)

    if User.objects.filter(username="admin").exists():
        return HttpResponse("Admin already exists")

    user = User.objects.create_superuser(
        username="admin",
        password="Admin@123",
        email="admin@example.com"
    )
    return HttpResponse("Admin created successfully!")
