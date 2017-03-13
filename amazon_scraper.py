import logging
from time import sleep

import requests
import validators
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# https://www.amazon.co.jp/product-reviews/B00Z16VF3E/ref=cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews&showViewpoints=1&sortBy=helpful&pageNumber=1


def extract_product_ids_from_link(category_link):
    category_link_soup = get_soup(category_link)
    products_links_1 = [a.attrs['href'] for a in category_link_soup.find_all('a')
                        if 'href' in a.attrs and '/gp/product/' in a.attrs['href']]
    products_links_2 = [a.attrs['href'] for a in category_link_soup.find_all('a')
                        if 'href' in a.attrs and '/dp/' in a.attrs['href']]
    products_links = products_links_1 + products_links_2
    products_ids = list(set(map(extract_product_id, products_links)))
    return products_ids


def get_random_product_ids():
    main_category_url = 'https://www.amazon.co.jp/gp/site-directory/ref=nav_shopall_btn'
    main_category_page = get_soup(main_category_url)
    category_links_soup = main_category_page.find_all('a', {'class': 'nav_a'})
    category_links = [a.attrs['href'] for a in category_links_soup]
    all_product_ids = set()
    links_visited = set()
    categories_count = len(category_links)
    logging.info('{} categories found.'.format(categories_count))
    i = 0
    while len(category_links) > 0:
        i += 1
        logging.info('-' * 80)
        logging.info('Stack length = {}, iterations = {}, total links visited = {}'.format(len(category_links), i,
                                                                                           len(links_visited)))
        category_link = category_links.pop()

        if category_link in links_visited:
            logging.info('ALREADY VISITED')
            continue
        else:
            links_visited.add(category_link)

        try:
            category_link_soup = get_soup(category_link)
            new_links = [a.attrs['href'] for a in category_link_soup.find_all('a')
                         if 'href' in a.attrs and a.attrs['href'].startswith('/s/')]  # or /b/
            category_links.extend(new_links)
            products_ids = extract_product_ids_from_link(category_link)
            logging.info(products_ids)
            for product_id in products_ids:
                all_product_ids.add(product_id)
            logging.info('{} products found at this step.'.format(len(products_ids)))
            logging.info('{} unique products found so far.'.format(len(all_product_ids)))
            if len(products_ids) > 0:
                for jj in range(2, 10):
                    if 'page' in category_link:
                        break
                    category_links.append(category_link + '&page={}'.format(jj))
        except Exception as e:
            logging.error('Exception occurred. Skipping')
            logging.error(e)


def get_product_reviews_url(item_id, page_number):
    return 'https://www.amazon.co.jp/product-reviews/{}/ref=' \
           'cm_cr_arp_d_paging_btm_1?ie=UTF8&reviewerType=all_reviews' \
           '&showViewpoints=1&sortBy=helpful&pageNumber={}'.format(
        item_id, page_number)


def extract_product_id(link_from_main_page):
    # e.g. B01H8A7Q42
    p_id = -1
    tags = ['/dp/', '/gp/product/']
    for tag in tags:
        try:
            p_id = link_from_main_page[link_from_main_page.index(tag) + len(tag):].split('/')[0]
        except:
            pass
    return p_id


def get_soup(url):
    if 'amazon.co.jp' not in url:
        url = 'https://www.amazon.co.jp' + url
    nap_time_sec = 0.5
    logging.debug('Script is going to sleep for {} (Amazon throttling). ZZZzzzZZZzz.'.format(nap_time_sec))
    sleep(nap_time_sec)
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
        item_id = extract_product_id(link)

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
    get_random_product_ids()
    # main()
