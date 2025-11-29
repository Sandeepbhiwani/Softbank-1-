from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Import migration helpers from home.views
from home.views import run_migrations
from home.views import run_fake   # <-- added fake migration runner

urlpatterns = [
    path('admin/', admin.site.urls),

    # Home pages
    path('', include('home.urls')),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('payments/', include('payments.urls')),
    path('assets/', include('assets.urls')),
    path('stock/', include('stockmanagement.urls')),
    path('dashboard/', include('dashboard.urls')),

    # Migration endpoints
    path("run-migrations/", run_migrations),  # full migration
    path("run-fake/", run_fake),              # fake apply migration
]

# STATIC & MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
