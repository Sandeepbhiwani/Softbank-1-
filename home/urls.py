from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contactus, name='contactus'),
    path('run-migrations/', run_migrations, name='run-migrations'),
    # path('aboutus/', aboutus, name='aboutus'),
    # path('privacypolicy/', privacypolicy, name='privacypolicy'),
    # path('termsofservice/', termsofservice, name='termsofservice'),
    # path('refundpolicy/', refundpolicy, name='refundpolicy'),
    path("run-collectstatic/", views.run_collectstatic, name="run_collectstatic"),
    path("run-createadmin/", views.run_createadmin, name="run_createadmin"),
]
