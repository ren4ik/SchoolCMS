from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('handbook/', include('handbook.urls')),
    path('staff/', include('staff.urls')),
    path('client/', include('client.urls')),
    path('classroom/', include('classroom.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
