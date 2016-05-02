from functools import lru_cache, partial
from urllib.parse import urljoin

from django.conf import settings
from django.core.urlresolvers import reverse as r
from django.db import models
from django.utils.translation import ugettext as _
import tweepy

from backend.base.models import LogEntry, Source


class TwitterSource(Source):

    """Connection to the Twitter API
    """

    _name = 'twitter'

    @classmethod
    def get_auth_class(cls):
        return partial(
            tweepy.OAuthHandler,
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET,
        )

    @classmethod
    def authorize(cls, request):
        OAuthHandler = cls.get_auth_class()

        # First step of OAuth dance: get token verifier
        if 'oauth_verifier' not in request.GET:
            callback_url = urljoin(
                request.build_absolute_uri(),
                r('sources:create_for', kwargs={'name': 'twitter'}))
            auth = OAuthHandler(callback_url)
            url = auth.get_authorization_url()
            request.session['twitter_request_token'] = auth.request_token
            return url  # Twitter authorization URL

        # Second step of OAuth dance: exchange request token for access token
        else:
            auth = OAuthHandler()
            auth.request_token = request.session.pop('twitter_request_token')
            auth.get_access_token(request.GET['oauth_verifier'])
            cls.objects.create(
                user=request.user,
                access_token=auth.access_token,
                access_token_secret=auth.access_token_secret,
            )
            return r('sources:list')

    @property
    @lru_cache()
    def api(self):
        """Authorize API access with saved tokens
        """
        OAuthHandler = self.get_auth_class()
        auth = OAuthHandler()
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth)

    def get_new_statuses(self):
        """Download new user statuses from Twitter
        """
        try:
            latest = TwitterLogEntry.objects.filter(
                _type=TwitterLogEntry.TYPE_TWEET,
                source=self,
            ).latest('datetime')
        except LogEntry.DoesNotExist:
            cursor = tweepy.Cursor(self.api.user_timeline)
        else:
            since_id = latest.external_id
            cursor = tweepy.Cursor(self.api.user_timeline, since_id=since_id)

        yield from cursor.items()

    def get_new_data(self):
        """Looks up on Twitter for new user data
        """
        for status in self.get_new_statuses():
            TwitterLogEntry.objects.create(
                _type=TwitterLogEntry.TYPE_TWEET,
                datetime=status.created_at,
                external_id=status.id,
                source=self,
                text=status.text,
                user=self.user,
            )

    class Meta:
        verbose_name = _('Twitter')
        verbose_name_plural = _('Connections to Twitter')


class TwitterLogEntry(LogEntry):

    """Representation of a Twitter object (tweet or direct message)
    """

    _entry_type = 'twitter'

    TYPE_TWEET = 't'
    TYPE_INCOMING_DIRECT_MESSAGE = 'i'
    TYPE_OUTCOMING_DIRECT_MESSAGE = 'o'

    _type = models.CharField(
        choices=[
            (TYPE_TWEET, _('Tweet')),

            # TODO: Add support
            (TYPE_INCOMING_DIRECT_MESSAGE, _('Incoming Direct Message')),
            (TYPE_OUTCOMING_DIRECT_MESSAGE, _('Outcoming Direct Message')),
        ],
        max_length=1,
    )
    external_id = models.BigIntegerField(
        verbose_name=_('Object ID on Twitter'),
    )
    text = models.TextField(
        help_text=_('Full text context. Usually 140 characters tops.'),
        verbose_name=_('text'),
    )
    datetime = models.DateTimeField(
        verbose_name=_('date and time'),
        help_text=_('Date and time the object was sent or received.'),
    )

    class Meta:
        verbose_name = _('Twitter object')
        verbose_name_plural = _('Twitter objects')
