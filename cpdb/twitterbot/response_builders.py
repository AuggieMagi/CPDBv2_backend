import itertools

from django.conf import settings
from django.template import Context, Template

from .models import TYPE_SINGLE_OFFICER, TYPE_COACCUSED_PAIR, TYPE_NOT_FOUND
from data.models import Allegation
from twitterbot.models import TweetResponseRoundRobin


class BaseResponseBuilder:
    def build(self, entities=None, extra_variables=None, context=None):
        for variables_set in self.get_variables_sets(entities, context):
            if extra_variables:
                variables_set.update(extra_variables)
            response_template = TweetResponseRoundRobin.objects.get_template(
                username=variables_set['user_name'], response_type=self.response_type)
            if context is not None:
                context.setdefault('responses_count', 0)
                context['responses_count'] += 1
            source = variables_set.get('source', ())
            url = variables_set.get('_url', '')
            tweet_content = Template(response_template.syntax).render(Context(variables_set))
            media_path = variables_set.get('_media_path', '')
            entity = variables_set.get('_entity', None)
            if len(tweet_content) > 140:
                tweet_content = tweet_content.replace('@{user_name} '.format(user_name=variables_set['user_name']), '')
            yield {
                'source': source,
                'tweet_content': tweet_content,
                'entity': entity,
                'url': url,
                'type': self.response_type,
                'media_path': media_path,
            }


class SingleOfficerResponseBuilder(BaseResponseBuilder):
    response_type = TYPE_SINGLE_OFFICER

    def get_variables_sets(self, entities, context):
        for (source, officer) in entities:
            yield {
                'officer': officer,
                '_entity': officer,
                '_url': '%s%s' % (settings.DOMAIN, officer.get_absolute_url()),
                'source': (source, ),
                '_media_path': officer.visual_token_png_path
            }


class CoaccusedPairResponseBuilder(BaseResponseBuilder):
    response_type = TYPE_COACCUSED_PAIR

    def get_variables_sets(self, entities, context):
        for (source1, officer1), (source2, officer2) in itertools.combinations(entities, 2):
            coaccused = Allegation.objects.filter(officerallegation__officer=officer1)\
                .filter(officerallegation__officer=officer2).distinct().count()
            if coaccused > 0:
                yield {
                    'officer1': officer1,
                    'officer2': officer2,
                    'coaccused': coaccused,
                    'source': (source1, source2)
                }


class NotFoundResponseBuilder(BaseResponseBuilder):
    response_type = TYPE_NOT_FOUND

    def get_variables_sets(self, entities, context):
        try:
            tweet = context.get('incoming_tweet', None)
            if context.get('responses_count', 0) > 0:
                raise StopIteration()
            if tweet.is_retweet_of_twitterbot:
                raise StopIteration()
            if tweet.is_quoted_tweet_of_twitterbot:
                raise StopIteration()
            if not tweet.is_mentioning_twitterbot:
                raise StopIteration()
        except AttributeError:
            raise StopIteration()
        yield {
            '_url': settings.DOMAIN
        }