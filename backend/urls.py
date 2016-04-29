from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    # Admin UI
    url(r'^admin/', admin.site.urls),

    # URLs from `webview`
    url(r'', include('backend.webview.urls')),
]
