from django.core.urlresolvers import reverse as r
from django.views import generic


class HomeView(generic.RedirectView):

    """A dumb home view that redirects to an actual one
    """

    def get_redirect_url(self):
        return r('log:log')
