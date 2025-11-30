from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contactus, name='contactus'),

    # Migration utilities
    path('run-migrations/', views.run_migrations, name='run-migrations'),
    path('run-collectstatic/', views.run_collectstatic, name='run_collectstatic'),
    path('run-createadmin/', views.run_createadmin, name='run_createadmin'),
    path('run-fake/', views.run_fake, name='run_fake'),
     path("run-createadmin-pg/", create_admin_pg, name="create_admin_pg"),

    # Optional pages (uncomment if needed)
    # path('aboutus/', views.aboutus, name='aboutus'),
    # path('privacypolicy/', views.privacypolicy, name='privacypolicy'),
    # path('termsofservice/', views.termsofservice, name='termsofservice'),
    # path('refundpolicy/', views.refundpolicy, name='refundpolicy'),
]
