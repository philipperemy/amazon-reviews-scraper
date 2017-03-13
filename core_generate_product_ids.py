import logging
import random

from core_utils import get_soup, extract_product_id


def extract_product_ids_from_link(category_link):
    category_link_soup = get_soup(category_link)
    products_links_1 = [a.attrs['href'] for a in category_link_soup.find_all('a')
                        if 'href' in a.attrs and '/gp/product/' in a.attrs['href']]
    products_links_2 = [a.attrs['href'] for a in category_link_soup.find_all('a')
                        if 'href' in a.attrs and '/dp/' in a.attrs['href']]
    products_links = products_links_1 + products_links_2
    products_ids = list(map(extract_product_id, products_links))
    return products_ids


def get_random_product_ids():
    main_category_page = get_soup('https://www.amazon.co.jp/gp/site-directory/ref=nav_shopall_btn')
    # can have more by clicking on those buttons.
    category_links_soup = main_category_page.find_all('a', {'class': 'nav_a'})
    category_links = [a.attrs['href'] for a in category_links_soup]
    all_product_ids = set()

    if len(category_links) == 0:
        logging.error('Cannot get categories from Amazon. Calling get_random_product_ids() again.')
        logging.error('It can possibly lead to an infinite loop.')
        get_random_product_ids()

    more_category_links = list(category_links)
    for i, category_link in enumerate(category_links):
        try:
            logging.info('({}/{}) get as many links as we can.'.format(i, len(category_links)))
            category_link_soup = get_soup('https://www.amazon.co.jp' + category_link)
            new_links = [a.attrs['href'] for a in category_link_soup.find_all('a')
                         if 'href' in a.attrs and a.attrs['href'].startswith('/s/')]  # or /b/
            more_category_links.extend(new_links)
            logging.info('{} links found so far.'.format(len(more_category_links)))
        except Exception as e:
            logging.error('Exception occurred. Skipping')
            logging.error(e)

    random.seed(123)
    random.shuffle(more_category_links)

    i = 0
    while len(more_category_links) > 0:
        i += 1
        logging.info('Stack length = {}'.format(len(more_category_links)))
        category_link = more_category_links.pop()
        try:
            logging.info('({}/{}) get as many products as we can.'.format(i, len(more_category_links)))
            products_ids = extract_product_ids_from_link(category_link)
            logging.info(products_ids)
            for product_id in products_ids:
                all_product_ids.add(product_id)
            logging.info('{} products found at this step.'.format(len(products_ids)))
            logging.info('{} unique products found so far.'.format(len(all_product_ids)))

            if len(products_ids) > 0:
                for jj in range(2, 30):
                    if 'page' in category_link:
                        break
                    more_category_links.append(category_link + '&page={}'.format(jj))
                    # https://www.amazon.co.jp/s/ref=sr_pg_2?fst=as%3Aoff&rh=n%3A57239051%2Cn%3A%2157240051%2Cn%3A71588051%2Cn%3A71649051%2Cp_n_feature_eight_browse-bin%3A2422256051&page=2&bbn=71649051&ie=UTF8&qid=1489379299

                    # https://www.amazon.co.jp/s/ref=lp_71649051_nr_p_n_feature_eight_br_0/351-3794295-4542940?fst=as%3Aoff&rh=n%3A57239051%2Cn%3A%2157240051%2Cn%3A71588051%2Cn%3A71649051%2Cp_n_feature_eight_browse-bin%3A2422256051&bbn=71649051&ie=UTF8&qid=1489378532&rnid=2422255051&page=2

        except Exception as e:
            logging.error('Exception occurred. Skipping')
            logging.error(e)
