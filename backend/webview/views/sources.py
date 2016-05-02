from functools import lru_cache

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse as r
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views import generic

from backend.base.models import Source
from backend.base.workers import get_new_data


class UserSourcesListView(LoginRequiredMixin, generic.ListView):

    """List all connected sources of an user
    """

    page_title = _('My connected log sources')
    template_name = 'sources/list.jade'

    def get_queryset(self):
        return Source.objects.filter(user=self.request.user)


class UserSourcePreCreateView(LoginRequiredMixin, generic.TemplateView):

    """Let users select a provider to connect to a log source
    """

    page_title = _('Connect to a new source')
    template_name = 'sources/pre-create.jade'

    def get_context_data(self, **kwargs):
        data = super(UserSourcePreCreateView, self).get_context_data(**kwargs)

        # Build a list of links to source type-specific creation views
        data['creation_links'] = [
            (
                source_model._meta.verbose_name,
                r('sources:create_for', kwargs={'name': source_model._name})
            )
            for source_model in Source.__subclasses__()
        ]

        return data


class UserSourceCreateView(LoginRequiredMixin, generic.RedirectView):

    """Let users connect to a log source

    Each log source adapter (logger) will provide an `authorize` method which
    must perform the connection steps while returning an URL to redirect to,
    either to an external authorizarion procedure (e.g. OAuth) or, finally, an
    URL within this application.
    """

    @lru_cache(maxsize=None)
    def get_model(self):
        """Get the model according to `name` URL kwarg
        """
        models_map = {
            model._name: model
            for model in Source.__subclasses__()
        }
        return models_map[self.kwargs['name']]

    def get_redirect_url(self, *args, **kwargs):
        # Bridge the request to the provider connection
        model = self.get_model()
        return model.authorize(self.request)


class ManualSourceSyncView(LoginRequiredMixin, generic.RedirectView):

    """Allow the user to manually get data from a source
    """

    def get_object(self):
        return get_object_or_404(
            Source, user=self.request.user, pk=self.kwargs['pk'])

    def get_redirect_url(self, pk):
        # Enqueue `source.get_new_data`
        get_new_data.delay(self.get_object())

        # Message the user
        messages.success(self.request, _(
            'Synchronization will happen soon. Stay tuned!'
        ))

        # Get back to sources list
        return r('sources:list')
