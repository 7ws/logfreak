from django.contrib import auth
from django.core.urlresolvers import reverse as r


class TestLoginView:

    """Tests for backend.webview.views.auth.LoginView

    These tests exist because the built-in Django view is actually wrapped.
    """

    def test_requesting_the_view_wont_crash(self, admin_client):
        """Check if the view is accessible
        """
        url = r('auth:login')
        resp = admin_client.get(url)
        assert resp.status_code == 200

    def test_brings_view_variable_to_template_context(self, client):
        """The `view` variable is available to the template context
        """
        resp = client.get(r('auth:login'))
        assert 'view' in resp.context

    def test_actually_logs_an_user_in(self, client, admin_user):
        """Make sure the user can be logged in
        """
        resp = client.post(
            r('auth:login'),
            data={'username': 'admin', 'password': 'password'},
            follow=True)
        assert resp.redirect_chain == [(r('home'), 302), (r('log:log'), 302)]

    def test_validates_login_form(self, client, admin_user):
        """Check the built-in authentication form validation against database
        """
        resp = client.post(
            r('auth:login'),
            data={'username': 'admin', 'password': 'wrong_password'})
        assert resp.status_code == 200
        assert resp.context['form'].errors


class TestLogoutView:

    """Tests for backend.webview.views.auth.LogoutView

    These tests exist because the built-in Django view is actually wrapped.
    """

    def test_logs_an_user_out(self, admin_client):
        """Make sure the the user can be logged out
        """
        admin_client.get(r('auth:logout'))
        user = auth.get_user(admin_client)
        assert not user.is_authenticated()

    def test_redirects_back_to_login(self, admin_client):
        """Check if the built-in redirection functionality is kept
        """
        resp = admin_client.get(r('auth:logout'), follow=True)
        assert resp.redirect_chain == [(r('auth:login'), 302)]
