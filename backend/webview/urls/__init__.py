from django.conf.urls import include, url


urlpatterns = [
    # Authentication
    url(r'^auth/', include('backend.webview.urls.auth', namespace='auth')),

    # Main views
    url(r'', include('backend.webview.urls.main')),  # No namespace!
    url(r'', include('backend.webview.urls.log', namespace='log')),
    url(
        r'^sources/',
        include('backend.webview.urls.sources', namespace='sources')),
]
