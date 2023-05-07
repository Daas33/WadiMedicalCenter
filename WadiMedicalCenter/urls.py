from django.views.static import serve
from django.urls import re_path
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import  static
urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include('account.urls')),
    path('appointment/',include('appointment.urls')),
    path('patient/',include('patient.urls' )),
    path('appmanager/',include('appmanager.urls')),
    
] 
# + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]