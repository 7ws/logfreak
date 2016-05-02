from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views import generic

from backend.base.models import Source


class UserSourcesListView(LoginRequiredMixin, generic.ListView):

    """List all connected sources of an user
    """

    page_title = _('My connected log sources')
    template_name = 'sources/list.jade'

    def get_queryset(self):
        return Source.objects.filter(user=self.request.user)
