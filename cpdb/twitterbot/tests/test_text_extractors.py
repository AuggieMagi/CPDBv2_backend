from django.test import SimpleTestCase

from robber import expect
from mock import patch

from twitterbot.text_extractors import TweetTextExtractor, HashTagTextExtractor, URLContentTextExtractor
from twitterbot.factories import TweetFactory, MockTweepyWrapperFactory


class TweetTextExtractorTestCase(SimpleTestCase):
    def test_extract(self):
        extractor = TweetTextExtractor()
        tweet = TweetFactory(text='abc')
        expect(extractor.extract(tweet)).to.eq([('text', 'abc')])

    def test_extract_remove_mention(self):
        extractor = TweetTextExtractor()
        expect(extractor.extract(TweetFactory(text='@def hey @twilight abc'))).to.eq([('text', 'hey abc')])


class HashTagTextExtractorTestCase(SimpleTestCase):
    def test_extract(self):
        extractor = HashTagTextExtractor()
        expect(extractor.extract(TweetFactory(hashtags=['johnDoe']))).to.eq([('#johnDoe', 'John Doe')])
        expect(extractor.extract(TweetFactory(hashtags=['JohnDoe']))).to.eq([('#JohnDoe', 'John Doe')])


class URLContentTextExtractorTestCase(SimpleTestCase):
    def setUp(self):
        super(URLContentTextExtractorTestCase, self).setUp()
        self.extractor = URLContentTextExtractor()
        client = MockTweepyWrapperFactory()
        self.tweet = TweetFactory(
            urls=['http://fakeurl.com/articles/1/'],
            context={'client': client, 'for_user_id': 123}
        )

    def test_extract(self):
        with patch('twitterbot.text_extractors.web_parsing.parse', return_value='CPD'):
            expect(self.extractor.extract(self.tweet)).to.eq([('http://fakeurl.com/articles/1/', 'CPD')])

        with patch('twitterbot.text_extractors.web_parsing.parse', return_value='Chicago Police'):
            expect(self.extractor.extract(self.tweet)).to.eq([('http://fakeurl.com/articles/1/', 'Chicago Police')])

    def test_extract_with_content_not_contains_key_words(self):
        with patch('twitterbot.text_extractors.web_parsing.parse', return_value='some text'):
            expect(self.extractor.extract(self.tweet)).to.eq([])
