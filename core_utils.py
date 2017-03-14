import logging
import re
from time import sleep

import requests
from bs4 import BeautifulSoup


def extract_product_id(link_from_main_page):
    # e.g. B01H8A7Q42
    p_id = -1
    tags = ['/dp/', '/gp/product/']
    for tag in tags:
        try:
            p_id = link_from_main_page[link_from_main_page.index(tag) + len(tag):].split('/')[0]
        except:
            pass
    m = re.match('[A-Z0-9]{10}', p_id)
    if m:
        return m.group()
    else:
        return None


def get_soup(url):
    if 'amazon.co.jp' not in url:
        url = 'https://www.amazon.co.jp' + url
    nap_time_sec = 1
    logging.debug('Script is going to sleep for {} (Amazon throttling). ZZZzzzZZZzz.'.format(nap_time_sec))
    sleep(nap_time_sec)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
    }
    logging.debug('-> to Amazon : {}'.format(url))
    out = requests.get(url, headers=header)
    assert out.status_code == 200
    soup = BeautifulSoup(out.content, 'html.parser')
    if 'captcha' in str(soup):
        logging.error('Your bot has been detected. Please wait a while.')
        logging.error('Program will exit.')
        exit(1)

    return soup


if __name__ == '__main__':
    l = 'https://www.amazon.co.jp/海派物語-Shanghai-Story-チャイナドレス（レディース、女性用）ドラゴン-パーティー/dp/B01F401N1A/ref=sr_1_1?ie=UTF8&qid=1486377535&sr=8-1&keywords=wine+red'
    print(extract_product_id(l))
