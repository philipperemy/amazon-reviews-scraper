import logging

import requests
import validators
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# https://www.amazon.co.jp/product-reviews/B00Z16VF3E/ref=cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=1

def get_product_reviews_url(item_id, page_number):
    return 'https://www.amazon.co.jp/product-reviews/{}/ref=' \
           'cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews' \
           '&showViewpoints=1&sortBy=helpful&pageNumber={}'.format(
        item_id, page_number)


def extract_item_id(link_from_main_page):
    return link_from_main_page[link_from_main_page.index('/dp/') + len('/dp/'):].split('/')[0]  # e.g. B01H8A7Q42


def get_soup(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'
    }
    logging.debug('-> to Amazon : {}'.format(url))
    out = requests.get(url, headers=header)
    assert out.status_code == 200
    return BeautifulSoup(out.content, 'html.parser')


def main():
    search = 'BOTANIST ボタニカルシャンプー 490ml ＆ トリートメント 490g　モイストセット'
    url = 'http://www.amazon.co.jp/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords=' + \
          search + '&rh=i%3Aaps%2Ck%3A' + search
    soup = get_soup(url)
    items = []
    for a in soup.find_all('a', class_='s-access-detail-page'):
        if a.find('h2') is not None and validators.url(a.get('href')):
            name = str(a.find('h2').string)
            link = a.get('href')
            items.append((link, name))
    logging.info('Found {} items.'.format(len(items)))
    for (link, name) in items:
        logging.debug('link = {}, name = {}'.format(link, name))
        item_id = extract_item_id(link)

        for page_number in range(100):
            product_reviews_link = get_product_reviews_url(item_id, page_number)
            so = get_soup(product_reviews_link)

            cr_review_list_so = so.find(id='cm_cr-review_list')

            if cr_review_list_so is None:
                logging.info('No reviews for this item.')
                break

            reviews_list = cr_review_list_so.find_all(attrs={'class': 'a-section review'})

            if len(reviews_list) == 0:
                logging.info('No more reviews to unstack.')
                break

            for review in reviews_list:
                rating = review.find(attrs={'data-hook': 'review-star-rating'}).attrs['class'][2].split('-')[-1]
                body = review.find(attrs={'data-hook': 'review-body'}).text
                title = review.find(attrs={'data-hook': 'review-title'}).text

                logging.info('***********************************************')
                logging.info('TITLE    = ' + title)
                logging.info('RATING   = ' + rating)
                logging.info('CONTENT  = ' + body)
                logging.info('***********************************************\n')


if __name__ == '__main__':
    main()
