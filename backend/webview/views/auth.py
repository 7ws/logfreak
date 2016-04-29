from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.utils.translation import ugettext as _
from django.views import generic


class LoginView(generic.TemplateView):

    """Log an user in

    Wrap Django's built-in `login` view, allowing extensibility.
    """

    page_title = _('Log in')
    template_name = 'auth/login.jade'

    def dispatch(self, request, **kwargs):
        # Extend the view with correct parameters
        kwargs.update(
            template_name=self.template_name,
            extra_context=self.get_context_data(),
        )

        # Handle request to the function-based view
        return auth_views.login(request, **kwargs)


class LogoutView(generic.View):

    """Log an user out

    Wrap Django's built-in `logout_then_login` view, allowing extensibility.
    """

    def dispatch(self, request, **kwargs):
        # Message the user about successful logout
        messages.success(request, _('Logged out successfully!'))

        # Handle request to the function-based view
        return auth_views.logout_then_login(request, **kwargs)
