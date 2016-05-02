from functools import partial
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
    def authorize(cls, request):
        OAuthHandler = partial(
            tweepy.OAuthHandler,
            settings.TWITTER_CONSUMER_KEY,
            settings.TWITTER_CONSUMER_SECRET)

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
