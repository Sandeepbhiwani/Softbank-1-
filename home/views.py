from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.conf import settings
from django.core.management import call_command
from django.db import connection


# ----------------------------
# INTERNAL CHECK
# ----------------------------
def _is_migration_authorized(request):
    """
    Authorize migration only if:
    - ?key=<TEMP_MIGRATE_KEY> matches the env variable, OR
    - logged-in user is staff/superuser
    """
    expected_key = getattr(settings, "TEMP_MIGRATE_KEY", None)
    provided_key = request.GET.get("key")

    # If temp key exists AND matches
    if expected_key and provided_key and provided_key == expected_key:
        return True

    # Admin login allowed
    if (
        request.user.is_authenticated
        and (request.user.is_staff or request.user.is_superuser)
    ):
        return True

    return False


# ----------------------------
# MAIN PAGES
# ----------------------------
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
# RUN FULL MIGRATIONS SAFELY
# ----------------------------
def run_migrations(request):
    if not _is_migration_authorized(request):
        return HttpResponseForbidden("Not authorized to run migrations")

    try:
        # Ensure migrations are generated
        call_command("makemigrations", interactive=False, verbosity=0)

        # Apply migrations
        call_command("migrate", interactive=False, verbosity=0)

        # Release DB connection (RAM-safe)
        connection.close()

    except Exception as exc:
        return HttpResponse(f"Migration failed:<br><br>{exc}", status=500)

    return HttpResponse("✅ All migrations applied successfully!", status=200)


# ----------------------------
# FAKE MIGRATION RUNNER
# fixes conflict errors like:
# 'column already exists'
# ----------------------------
def run_fake(request):
    if not _is_migration_authorized(request):
        return HttpResponseForbidden("Not authorized to fake migrations")

    app = request.GET.get("app")
    name = request.GET.get("name")

    if not app or not name:
        return HttpResponse(
            "Missing parameters:<br><br>"
            "Use format:<br>"
            "/run-fake/?key=YOUR_KEY&app=APP_NAME&name=MIGRATION_FILE_NAME"
        )

    try:
        call_command("migrate", app, name, fake=True)
        connection.close()
    except Exception as exc:
        return HttpResponse(f"Fake migration failed:<br><br>{exc}", status=500)

    return HttpResponse(f"✅ FAKE applied: {app} → {name}", status=200)
