from unittest import mock

from django.core.urlresolvers import reverse as r

from backend.twitter_logger.models import TwitterSource


class TestTwitterSource:

    """Tests for `backend.twitter_logger.models.TwitterSource`
    """

    @mock.patch('backend.twitter_logger.models.tweepy.OAuthHandler')
    def test_authorize_passes_complete_callback_url(self, oauth, rf):
        """The `authorize` method passes a full callback URL (not just an URI).
        """
        request = rf.get('/auth')
        request.session = {}
        TwitterSource.authorize(request)
        args, kwargs = oauth.call_args
        assert args[-1].startswith('http://testserver/')

    @mock.patch('backend.twitter_logger.models.tweepy.OAuthHandler')
    def test_authorize_executes_first_oauth_step(self, oauth, rf):
        """The `authorize` method will first retrieve authorization URL
        """
        request = rf.get('/auth')
        request.session = {}
        url = TwitterSource.authorize(request)
        assert (
            request.session['twitter_request_token'] == oauth().request_token)
        assert url == oauth().get_authorization_url()

    @mock.patch('backend.twitter_logger.models.tweepy.OAuthHandler')
    def test_authorize_executes_second_oauth_step(self, oauth, rf, admin_user):
        """The `authorize` method will create a source after authorization
        """
        # Fill request with data normally brought from Twitter's OAuth
        request = rf.get('/auth?oauth_verifier=foobar')
        request.user = admin_user
        request.session = {'twitter_request_token': 'nothinghere'}

        # Fill OAuth instance with fake access tokens
        oauth().access_token = 'no-access'
        oauth().access_token_secret = 'not-a-secret'

        # Authorize and check auth info
        url = TwitterSource.authorize(request)
        source = TwitterSource.objects.latest('pk')
        assert source.user == admin_user
        assert source.access_token == 'no-access'
        assert source.access_token_secret == 'not-a-secret'

        # URL now should point to our app
        assert url == r('sources:list')
