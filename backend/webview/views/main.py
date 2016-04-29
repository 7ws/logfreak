from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic


class HomeView(LoginRequiredMixin, generic.View):

    """A dumb home view
    """

    def get(self, request):
        return HttpResponse('Welcome, {}!'.format(request.user))
