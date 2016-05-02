from functools import partial
from unittest import mock

from django.core.urlresolvers import reverse as r
import pytest

from backend.twitter_logger.models import TwitterLogEntry, TwitterSource


@pytest.fixture
def twitter_source(admin_user):
    """Create an test-able `TwitterSource` object
    """
    return TwitterSource.objects.create(
        user=admin_user,
        access_token='no-access',
        access_token_secret='not-a-secret',
    )


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

    @mock.patch('backend.twitter_logger.models.tweepy')
    def test_get_new_statuses_builds_timeline_cursor_with_since_id(
            self, tweepy, twitter_source, admin_user):
        """`get_new_statuses` uses most recent object's ID as `since_id`
        """
        new_status = partial(
            TwitterLogEntry.objects.create,
            _type=TwitterLogEntry.TYPE_TWEET,
            user=admin_user,
            source=twitter_source,
            text='Random tweet',
            external_id=123,
        )
        # Create a couple objects, intentionally in reverse order so that
        # any `.latest` call isn't biased by `pk`
        new_status(datetime='2000-01-01 01:00:00', external_id=100)
        new_status(datetime='2000-01-01 00:00:00', external_id=200)

        # Check Cursor call
        api_call = twitter_source.api.user_timeline
        list(twitter_source.get_new_statuses())
        tweepy.Cursor.assert_called_once_with(api_call, since_id=100)

    @mock.patch('backend.twitter_logger.models.tweepy')
    def test_get_new_statuses_builds_timeline_cursor_without_since_id(
            self, tweepy, twitter_source):
        """`get_new_statuses` uses no `since_id` when first-running
        """
        # Check Cursor call
        api_call = twitter_source.api.user_timeline
        list(twitter_source.get_new_statuses())
        tweepy.Cursor.assert_called_once_with(api_call)

    @mock.patch('backend.twitter_logger.models.tweepy')
    def test_get_new_data_downloads_statuses_into_database(
            self, tweepy, twitter_source, admin_user):
        # Configure fake API results for statuses
        tweepy.Cursor().items.return_value = [
            mock.Mock(
                id=100,
                text='Random tweet',
                created_at='2000-01-01T00:00:00+00:00',
            ),
        ]

        # Download data
        assert not TwitterLogEntry.objects.exists()
        twitter_source.get_new_data()

        # Check stored data
        assert TwitterLogEntry.objects.count() == 1
        status = TwitterLogEntry.objects.latest('pk')
        assert status.user == admin_user
        assert status.source == twitter_source
        assert status.external_id == 100
        assert status.text == 'Random tweet'
        assert status.datetime.isoformat() == '2000-01-01T00:00:00+00:00'
