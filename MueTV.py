#!/usr/bin/env python3
import json
import subprocess
import requests
import pprint


def get_mn_count():
    from bs4 import BeautifulSoup
    r = requests.get("https://chainz.cryptoid.info/mue/")
    soup = BeautifulSoup(r.text, 'html.parser')
    mns = soup.find("span", {"id": "masternodes"}).text.split('/')[0]
    return int(mns)


def get_mue_supply():
    r = requests.get(url="http://chainz.cryptoid.info/mue/api.dws?q=totalcoins")
    return r.json()


def get_btc_rate():
    r = requests.get(url="https://blockchain.info/ticker")
    rj = r.json()
    return rj


def get_mue_btc():
    r = requests.get(url="https://bittrex.com/api/v1.1/public/getmarketsummary?market=btc-mue")
    rj = r.json()
    if rj['success']:
        return rj['result']
    else:
        return None


def convert_to(c, v):
    r = requests.get(url="https://blockchain.info/tobtc?currency=" + c + "&value=" + v)
    return r


def data_to_json(d):
    with open("data.json", "w") as f:
        json.dump(d, f)


def build_data():
    daily_blocks = 2050
    mn_rewards_mue = 18
    mue_btc = get_mue_btc()[0]['High']
    btc_usd = get_btc_rate()['USD']['last']
    mue_usd = btc_usd * mue_btc
    mn_count = get_mn_count()
    mn_reward_avg = (daily_blocks * mn_rewards_mue) / mn_count
    data_pile = {
        "muedaily": mn_reward_avg,
        "usddaily": mn_reward_avg * mue_usd,
        "usdprice": mue_usd,
        "btcprice": mue_btc,
        "mncount": mn_count,
        "totalsupply": get_mue_supply(),
        "pricebtcusd": btc_usd
    }
    data_to_json(data_pile)


build_data()
