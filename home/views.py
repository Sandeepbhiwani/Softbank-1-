from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.core.management import call_command
from django.db import connection

def _is_migration_authorized(request):
    expected_key = getattr(settings, "TEMP_MIGRATE_KEY", None)
    provided_key = request.GET.get("key")

    # Temporary key allowed
    if expected_key and provided_key and provided_key == expected_key:
        return True

    # Logged-in admin allowed
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


# ----------------------------
# SAFE MIGRATION RUNNER
# ----------------------------
def run_migrations(request):
    if not _is_migration_authorized(request):
        return HttpResponseForbidden("Not authorized to run migrations")

    try:
        # Run each migration step individually
        call_command("makemigrations", interactive=False, verbosity=0)

        # Apply migrations in chunks to avoid Render timeout
        call_command("migrate", interactive=False, verbosity=0)

        # Force DB connection close (avoid RAM leaking)
        connection.close()

    except Exception as exc:
        return HttpResponse(f"Migration failed:<br><br>{exc}", status=500)

    return HttpResponse("✅ All migrations applied successfully!", status=200)
