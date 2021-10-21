from datetime import datetime, date, timedelta
import requests, json, re, os, time
from itertools import  count

from .conf.config import Config
from .logger import Logger

class News():
    def __init__(self, logger: Logger, config: Config):
        self.config = config
        self.logger = logger

        # user input variables
        # Values are keyowords to search the web for
        # Keys can be used to send a trading request if integrated with an Exchange
        self.crypto_key_pairs = {"BTCUSD":"Bitcoin", "ETHUSD":"Ethereum", "LTCUSD":"Litecoin", "XRPUSD":"Ripple", "BATUSD":"BATUSD, basic attention token", "DSHUSD":"Dash Coin", "EOSUSD":"EOS", "ETCUSD":"ETC", "IOTUSD":"IOTA", "NEOUSD":"NEO", "OMGUSD":"OMISE Go", "TRXUSD":"Tron", "XLMUSD":"Stellar Lumens", "XMRUSD":"Monero", "ZECUSD":"Zcash"}

        #define from published date
        self.date_since = date.today() - timedelta(days=1)

        #store inputs in different lists
        self.cryptocurrencies = []
        self.crypto_keywords = []

        #Storing keys and values in separate lists
        for i in range(len(self.crypto_key_pairs)):
            self.cryptocurrencies.append(list(self.crypto_key_pairs.keys())[i])
            self.crypto_keywords.append(list(self.crypto_key_pairs.values())[i])
    
    def get_news_headlines(self):
        '''Search the web for news headlines based the keywords in the global variable'''
        news_output = {}

        #TO DO - looping through keywords creates odd looking dicts. Gotta loop through keys instead.
        for crypto in self.crypto_keywords:

            #create empty dicts in the news output
            news_output["{0}".format(crypto)] = {'description': [], 'title': []}

            #configure the fetch request and select date range. Increase date range by adjusting timedelta(days=1)
            url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/search/NewsSearchAPI"
            querystring = {"q":str(crypto),"pageNumber":"1","pageSize":"30","autoCorrect":"true","fromPublishedDate":self.date_since,"toPublishedDate":"null"}
            headers = {
                'x-rapidapi-key': self.config.WEBSEARCH_KEY,
                'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
                }

            #get the raw response
            response = requests.request("GET", url, headers=headers, params=querystring)

            # convert response to text format
            result = json.loads(response.text)

            #store each headline and description in the dicts above
            for news in result['value']:
                news_output[crypto]["description"].append(news['description'])
                news_output[crypto]["title"].append(news['title'])

        return news_output

    def analyze_headlines(self):
        '''Analyse each headline pulled trhough the API for each crypto'''
        news_output = self.get_news_headlines()

        for crypto in self.crypto_keywords:

            #empty list to store sentiment value
            news_output[crypto]['sentiment'] = {'pos': [], 'mid': [], 'neg': []}

            # analyse the description sentiment for each crypto news gathered
            if len(news_output[crypto]['description']) > 0:
                for title in news_output[crypto]['title']:

                    # remove all non alphanumeric characters from payload
                    titles = re.sub('[^A-Za-z0-9]+', ' ', title)

                    import http.client
                    conn = http.client.HTTPSConnection('text-sentiment.p.rapidapi.com')

                    #format and sent the request
                    payload = 'text='+titles
                    headers = {
                        'content-type': 'application/x-www-form-urlencoded',
                        'x-rapidapi-key': self.config.SENTIMENT_KEY,
                        'x-rapidapi-host': 'text-sentiment.p.rapidapi.com'
                        }
                    conn.request("POST", "/analyze", payload, headers)

                    #get the response and format it
                    res = conn.getresponse()
                    data = res.read()
                    title_sentiment = json.loads(data)

                    #assign each positive, neutral and negative count to another list in the news output dict
                    if not isinstance(title_sentiment, int):
                        if title_sentiment['pos'] == 1:
                            news_output[crypto]['sentiment']['pos'].append(title_sentiment['pos'])
                        elif title_sentiment['mid'] == 1:
                            news_output[crypto]['sentiment']['mid'].append(title_sentiment['mid'])
                        elif title_sentiment['neg'] == 1:
                            news_output[crypto]['sentiment']['neg'].append(title_sentiment['neg'])
                        else:
                            print(f'Sentiment not found for {crypto}')

        return news_output
    
    def calc_sentiment(self):
        '''Use the sentiment returned in the previous function to calculate %'''
        news_output = self.analyze_headlines()

        #re-assigned the sentiment list value to a single % calc of all values in each of the 3 lists
        for crypto in self.crypto_keywords:

            #length of title list can't be 0 otherwise we'd be dividing by 0 below
            if len(news_output[crypto]['title']) > 0:

                news_output[crypto]['sentiment']['pos'] = len(news_output[crypto]['sentiment']['pos'])*100/len(news_output[crypto]['title'])
                news_output[crypto]['sentiment']['mid'] = len(news_output[crypto]['sentiment']['mid'])*100/len(news_output[crypto]['title'])
                news_output[crypto]['sentiment']['neg'] = len(news_output[crypto]['sentiment']['neg'])*100/len(news_output[crypto]['title'])

                #print the output  for each coin to verify the result
                print(crypto, news_output[crypto]['sentiment'])

        return news_output
