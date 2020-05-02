from django.conf.urls import url
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns

from .views import Subject

urlpatterns = [
    path('<slug>/', Subject.as_view(), name="slug")
]
