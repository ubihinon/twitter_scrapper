from datetime import datetime

from bs4 import BeautifulSoup


class TweetParser:
    def retrieve_tweets(self, limit, html):
        parser = BeautifulSoup(html, 'lxml')
        tweets = []

        for tweet in parser.body.find_all('div', attrs={'class': 'tweet'}, limit=limit):
            tweets.append(self.get_tweet(tweet))

        return tweets

    def get_tweet(self, bs_obj):
        return {
            'account': self.retrieve_account(bs_obj),
            'hashtags': self.retrieve_hashtags(bs_obj),
            'date': self.retrieve_date(bs_obj),
            'likes': self.retrieve_likes_count(bs_obj),
            'replies': self.retrieve_replies_count(bs_obj),
            'retweets': self.retrieve_retweets_count(bs_obj),
            'text': self.retrieve_text(bs_obj)
        }

    def retrieve_account(self, bs_obj):
        account_data = bs_obj.find(
            'a',
            attrs={'class': 'account-group'}
        )
        account = {
            'id': int(account_data.get('data-user-id')),
            'href': account_data.get('href'),
            'fullname': account_data.find('strong', attrs={'class': 'fullname'}).text
        }

        return account

    def retrieve_date(self, bs_obj):
        time = bs_obj.find('a', attrs={'class': 'tweet-timestamp'}).get('title')
        return datetime.strptime(time, '%I:%M %p - %d %b %Y').strftime('%-I:%M %p - %-d %b %Y')

    def retrieve_likes_count(self, bs_obj):
        return self._retrieve_count_value(bs_obj, 'ProfileTweet-action--favorite u-hiddenVisually')

    def retrieve_replies_count(self, bs_obj):
        return self._retrieve_count_value(bs_obj, 'ProfileTweet-action--reply u-hiddenVisually')

    def retrieve_retweets_count(self, bs_obj):
        return self._retrieve_count_value(bs_obj, 'ProfileTweet-action--retweet u-hiddenVisually')

    def retrieve_hashtags(self, bs_obj):
        containers = bs_obj.find_all('a', attrs={'data-query-source': 'hashtag_click'})
        return [c.text for c in containers]

    def retrieve_text(self, bs_obj):
        return bs_obj.find('p', attrs={'class': 'tweet-text'}).text

    def _retrieve_count_value(self, bs_obj, container_class_name):
        container = bs_obj.find('span', attrs={'class': container_class_name})
        count = container.find('span', attrs={'class': 'ProfileTweet-actionCount'}).get('data-tweet-stat-count')

        return int(count)
