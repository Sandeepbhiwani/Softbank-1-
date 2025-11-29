from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import requests
from .models import *
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.management import call_command


def _is_migration_authorized(request):
    """
    Allow migration runs when either:
     - ?key=<TEMP_MIGRATE_KEY> matches the environment variable (set in Render), or
     - the logged-in user is staff/superuser.

    NOTE: This route should be removed after use. It's intentionally temporary and
    protected only by a secret key or admin login. Never leave it open in production.
    """
    # If TEMP_MIGRATE_KEY is unset, only allow staff users
    expected_key = getattr(settings, 'TEMP_MIGRATE_KEY', None)
    provided_key = request.GET.get('key')
    if expected_key and provided_key and provided_key == expected_key:
        return True
    if request.user.is_authenticated and (
        getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False)
    ):
        return True
    return False

def home(request):
    return render(request,'home/home.html')

def aboutus(request):
    return render(request,'home/aboutus.html')

def contactus(request):
    return render(request,'home/contactus.html')

def privacypolicy(request):
    return render(request,'home/privacypolicy.html')

def termsofservice(request):
    return render(request,'home/termsofservice.html')

def refundpolicy(request):
    return render(request,'home/refundpolicy.html')

def error_404_view(request, exception):
    return render(request, 'home/404.html', status=404)


def run_migrations(request):
    """Temporary view to run database migrations on deploy.

    Usage examples:
    - https://yourapp/run-migrations/?key=<your-temp-key>
    - OR login as admin and visit the route while authenticated.
    """
    if not _is_migration_authorized(request):
        return HttpResponseForbidden('Not authorized to run migrations')
    # Run migrations and optionally collectstatic (if needed)
    try:
        call_command('migrate', interactive=False, verbosity=1)
        # call_command('collectstatic', interactive=False, verbosity=0)
    except Exception as exc:  # pragma: no cover - rudimentary error handling
        return HttpResponse(f"Migration failed: {exc}", status=500)
    return HttpResponse('Migrations completed!', status=200)