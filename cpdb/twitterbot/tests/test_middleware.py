from django.test import TestCase

from mock import Mock, patch
from robber import expect

from twitterbot.middleware import LogTwitterbotLinkVisitMiddleware
from twitterbot.factories import TwitterBotResponseLogFactory


class LogTwitterbotLinkVisitMiddlewareTestCase(TestCase):
    def test_log_twitterbot_link(self):
        response = Mock()
        get_response = Mock(return_value=response)
        middleware = LogTwitterbotLinkVisitMiddleware(get_response)
        request = Mock(GET={'twitterbot_log_id': 123}, path='/foo/')
        tweet_url = 'http://t.co/status/123/'
        TwitterBotResponseLogFactory(id=123, tweet_url=tweet_url)
        with patch('twitterbot.middleware.logger.info') as info:
            expect(middleware(request)).to.eq(response)
            info.assert_called_with('LogTwitterbotLinkVisitMiddleware - Someone visit /foo/ from status %s' % tweet_url)

    def test_no_log(self):
        response = Mock()
        get_response = Mock(return_value=response)
        middleware = LogTwitterbotLinkVisitMiddleware(get_response)
        request = Mock(GET={}, path='/foo/')
        with patch('twitterbot.middleware.logger.info') as info:
            expect(middleware(request)).to.eq(response)
            info.assert_not_called()