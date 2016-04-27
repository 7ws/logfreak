from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    # Admin UI
    url(r'^admin/', admin.site.urls),
]
