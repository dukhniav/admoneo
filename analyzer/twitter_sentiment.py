from .database import Database
from .logger import Logger
from .configuration.configuration import Config
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import datetime
import time
from nltk import tokenize

import pandas as pd
import tweepy

import queue
import threading
import nltk
nltk.download("stopwords")
nltk.download("wordnet")
nltk.download('punkt')


class TweetMiner():

    def __init__(self, config: Config, logger: Logger, database: Database):
        self.config = config
        self.logger = logger
        self.db = database
        self.should_publish = threading.Event()
        self.update_queue = queue.Queue()
        self.tweepy = tweepy

        self.result_limit = 20
        self.data = []
        self.api = False

        self.stop_words = stopwords.words("english")
        self.stemmer = SnowballStemmer("english", ignore_stopwords=True)
        self.lemmatizer = WordNetLemmatizer()

        logger.debug("initializing twitter api")
        self.client = tweepy.Client(self.config.TWITTER_BEARER_TOKEN, self.config.TWITTER_API_CONSUMER_KEY, self.config.TWITTER_API_CONSUMER_SECRET,
                                    self.config.TWITTER_ACCESS_TOKEN, self.config.TWITTER_ACCESS_TOKEN_SECRET, wait_on_rate_limit=True)

        logger.debug("twitter api initialized")

    def mine_crypto_currency_tweets(self):
        coins = self.db.get_all_coins()

        for coin in coins:
            coin_name = coin["coin_name"]
            self.logger.debug(
                "Getting Twitter sentiment for: " + coin_name)
            cypto_query = f"#{coin_name}"

            tweets = self.client.search_recent_tweets(
                cypto_query,
                max_results=25,
                tweet_fields=["context_annotations", "created_at"]
            )
            for tweet in tweets.data:
                sentiment = self.process_sentiment(tweet)
                self.db.add_tweet_sentiment(
                    coin["coin_base"], coin_name, sentiment, tweet.created_at)

    def process_sentiment(self, tweet):
        tokenized_text = tokenize.sent_tokenize(tweet.text.lower())
        words = [self.lemmatizer.lemmatize(w)
                 for w in tokenized_text if w not in self.stop_words]
        stem_text = " ".join([self.stemmer.stem(i) for i in words])
        analysis = TextBlob(stem_text)
        return analysis.sentiment.polarity

    def start_publisher(self):
        coin_list = self.db.get_all_coins()

        starttime = time.time()
        print("Start polling", starttime)
        poll_iteration = 1

        for i in range(10):
            for coin in coin_list:
                print(i, poll_iteration, "\rpublishing update ", end="")
                self.update_queue.put((poll_iteration, coin))
                poll_iteration += 1
                time.sleep(900)
                print("\rawaiting for publishing update", end="")
                self.should_publish.wait()
                self.update_queue.join()

    def start_update_listener(self):
        while True:
            poll_iteration, name = self.update_queue.get()

            # print(" --- ", name)
            try:

                self.mine_crypto_currency_tweets(query=name)
                self.update_queue.task_done()

            except Exception as e:  # work on python 3.x
                print("Failed to upload to ftp: " + str(e))

    listener_thread = threading.Thread(
        target=start_update_listener, daemon=True)
    publisher_thread = threading.Thread(target=start_publisher, daemon=True)
