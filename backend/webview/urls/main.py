from django.conf.urls import url

from ..views import main


urlpatterns = [
    url(r'^$', main.HomeView.as_view(), name='home'),
]
