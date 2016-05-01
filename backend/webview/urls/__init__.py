from django.conf.urls import include, url


urlpatterns = [
    # Authentication
    url(r'^auth/', include('backend.webview.urls.auth', namespace='auth')),

    # Main views
    url(r'', include('backend.webview.urls.main')),
    url(r'', include('backend.webview.urls.log_entries')),
]
