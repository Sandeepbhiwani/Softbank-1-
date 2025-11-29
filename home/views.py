from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.core.management import call_command

def _is_migration_authorized(request):
    """
    Migration allowed only if:
    - ?key=<TEMP_MIGRATE_KEY> matches environment variable, OR
    - user is admin/staff.
    """
    expected_key = getattr(settings, "TEMP_MIGRATE_KEY", None)
    provided_key = request.GET.get("key")

    # Allow via temp key
    if expected_key and provided_key and provided_key == expected_key:
        return True

    # Allow logged-in admin
    if (
        request.user.is_authenticated 
        and (request.user.is_staff or request.user.is_superuser)
    ):
        return True

    return False


def home(request):
    return render(request, "home/home.html")

def aboutus(request):
    return render(request, "home/aboutus.html")

def contactus(request):
    return render(request, "home/contactus.html")

def privacypolicy(request):
    return render(request, "home/privacypolicy.html")

def termsofservice(request):
    return render(request, "home/termsofservice.html")

def refundpolicy(request):
    return render(request, "home/refundpolicy.html")

def error_404_view(request, exception):
    return render(request, "home/404.html", status=404)


def run_migrations(request):
    if not _is_migration_authorized(request):
        return HttpResponseForbidden("Not authorized to run migrations")

    try:
        call_command("migrate", interactive=False, verbosity=1)
    except Exception as exc:
        return HttpResponse(f"Migration failed: {exc}", status=500)

    return HttpResponse("Migrations completed!", status=200)
