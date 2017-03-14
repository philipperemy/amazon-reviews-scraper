import logging
import random

from banned_exception import BannedException
from core_utils import get_soup, extract_product_id


def extract_product_ids_from_link(category_link):
    category_link_soup = get_soup(category_link)
    products_links_1 = [a.attrs['href'] for a in category_link_soup.find_all('a')
                        if 'href' in a.attrs and '/gp/product/' in a.attrs['href']]
    products_links_2 = [a.attrs['href'] for a in category_link_soup.find_all('a')
                        if 'href' in a.attrs and '/dp/' in a.attrs['href']]
    products_links = products_links_1 + products_links_2
    products_ids = list(map(extract_product_id, products_links))
    products_ids = list(filter(None.__ne__, products_ids))  # remove None values
    return products_ids


def get_random_product_ids(output_filename):
    # this function has a random behavior! It's like restoring from a checkpoint
    # because a new call will yield new values.
    logging.info('Writing to {}'.format(output_filename))
    with open(output_filename, 'w') as o:
        main_category_page = get_soup('https://www.amazon.co.jp/gp/site-directory/ref=nav_shopall_btn')
        # can have more by clicking on those buttons.
        category_links_soup = main_category_page.find_all('a', {'class': 'nav_a'})
        category_links = [a.attrs['href'] for a in category_links_soup]
        all_product_ids = set()
        more_category_links = list(category_links)
        for it, category_link in enumerate(category_links):
            try:
                logging.info('({}/{}) get as many links as we can.'.format(it, len(category_links)))
                category_link_soup = get_soup(category_link)
                new_links = [a.attrs['href'] for a in category_link_soup.find_all('a')
                             if 'href' in a.attrs and a.attrs['href'].startswith('/s/')]  # or /b/
                more_category_links.extend(new_links)
                logging.info('{} links found so far.'.format(len(more_category_links)))
            except BannedException as be:
                raise be
            except Exception as e:
                logging.error('Exception occurred. Skipping')
                logging.error(e)

        random.shuffle(more_category_links)

        it = 0
        while len(more_category_links) > 0:
            it += 1
            logging.info('Stack length = {}'.format(len(more_category_links)))
            category_link = more_category_links.pop()
            try:
                logging.info('({}/{}) get as many products as we can.'.format(it, len(more_category_links)))
                cur_product_ids = extract_product_ids_from_link(category_link)
                logging.info(cur_product_ids)
                for product_id in cur_product_ids:
                    if product_id not in all_product_ids:
                        all_product_ids.add(product_id)
                        o.write('{}\n'.format(product_id))
                        o.flush()
                logging.info('{} products found at this step.'.format(len(cur_product_ids)))
                logging.info('{} unique products found so far.'.format(len(all_product_ids)))

                if len(cur_product_ids) > 0:
                    for jj in range(2, 50):
                        if 'page' in category_link:
                            break
                        more_category_links.append(category_link + '&page={}'.format(jj))
            except BannedException as be:
                raise be
            except Exception as e:
                logging.error('Exception occurred. Skipping')
                logging.error(e)
