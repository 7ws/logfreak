from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Django-RQ management
    url(r'^admin/rq/', include('django_rq.urls')),

    # Admin UI
    url(r'^admin/', admin.site.urls),

    # URLs from `webview`
    url(r'', include('backend.webview.urls')),
]
