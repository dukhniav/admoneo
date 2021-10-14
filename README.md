# analyzer

Python script to continuously analyze crypto data.

## Table of contents

1. [Tool Setup](#tool-setup)
   1. [Install Python dependencies](#Install-Python-dependencies)
   2. [Create user configuration](#Create-user-configuration)
      1. [Environment Variables](#Environment-Variables)
      2. [MongoDB Atlas](#MongoDB-Atlas)
   3. [Run analyzer](#Run)
2. [Background](#Background)
3. [Open to-dos](#future-to-dos)

---

## Tool Setup

### Install Python dependencies

Run the following line in the terminal: `pip install -r requirements.txt`.

### Create user configuration

Create a .cfg file named `user.cfg` based off `.user.cfg.example`

**The configuration file consists of the following fields:**

- **exchange** - CoinGecko exchange to pull coin info from
- **mongo_user** - MongoDB Atlas username - used only when using cloud mongo
- **mongo_pw** - MongoDB Atlas password - used only when using cloud mongo
- **bot_sleep_time** - Interval time (in minutes) between CoinGecko API calls to get new data

#### Environment Variables

1.  In `/config/`, copy and rename user_template.cfg to user.cfg and fill in coin-gecko exchange
    - Example:
      ```console
      exchange=pancakeswap_new
      ```
    2.  You can view a list of CoinGecko exchanges [here](https://api.coingecko.com/api/v3/exchanges/list)
2.  Install Mongo ([Instructions](https://docs.mongodb.com/guides/server/install/)) 1. Verify Mongo installation by running:
    `console $ mongod --version ` 2. Start Mongo by running locally:
    `console $ brew services start mongodb-community ` \* more [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-os-x/)
    > Alternatively, MongoDB Atlas can be used.

#### MongoDB Atlas

3.  Register for a [Mongo Atlas](https://www.mongodb.com/cloud/atlas/register) account and create a free (or paid) cluster
4.  Verify your version of Python is correct by clicking on "Connect > Connect your application" 5. If not, update `self.MONGO_URL` in `/analyzer/conf/config.py` with correct URL
5.  Copy username and password to user.cfg:
    ```
    mongo_user=
    mongo_pw=
    ```
6.  Comment out line 19 in `/analyzer/database.py`
    `19: self.client = MongoClient('127.0.0.1', 27017)`
7.  Uncomment line 22 in `/analyzer/database.py`:
    `21: self.client = MongoClient(config.MONGO_URL)`

### Run

```shell
python -m analyzer
```

## Background

Background info here

## Future To-dos

[] [Daily news sentiment](https://www.cryptomaton.org/2021/04/05/how-to-analyse-daily-news-sentiment-for-cryptocurrency-with-python/)
[] [Analyzing crypto markets](https://blog.patricktriest.com/analyzing-cryptocurrencies-python/)
[] [Price prediction](https://towardsdatascience.com/demystifying-cryptocurrency-price-prediction-5fb2b504a110?gi=f6a5372b8e94)
[] [Fundemental analysis](https://academy.binance.com/en/articles/a-guide-to-cryptocurrency-fundamental-analysis)
[] [Indicators to watch](https://tradecraftjake.medium.com/cryptoasset-fundamental-analysis-7-indicators-ratios-to-watch-470c56076c2e)
[] [Custom calculations](https://hackernoon.com/advanced-cryptocurrency-market-analysis-via-custom-calculations-ih1j3xix)
[] [Crypto assessment methods](https://towardsdatascience.com/simple-method-to-assess-your-next-crypto-investment-9443f56ee4bf)
