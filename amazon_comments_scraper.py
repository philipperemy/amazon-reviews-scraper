import argparse

from core_extract_comments import *
from core_utils import *


def run(search, input_product_ids_filename):
    if input_product_ids_filename is not None:
        with open(input_product_ids_filename, 'r') as r:
            product_ids = [p.strip() for p in r.readlines()]
            logging.info('{} product ids were found.'.format(len(product_ids)))
            reviews_counter = 0
            for product_id in product_ids:
                _, exist = get_reviews_filename(product_id)
                if exist:
                    logging.info('product id [{}] was already fetched. Skipping.'.format(product_id))
                    continue
                reviews = get_comments_with_product_id(product_id)
                reviews_counter += len(reviews)
                logging.info('{} reviews found so far.'.format(reviews_counter))
                persist_comment_to_disk(reviews)
    else:
        default_search = 'iPhone'
        search = default_search if search is None else search
        reviews = get_comments_based_on_keyword(search)
        persist_comment_to_disk(reviews)


def get_script_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    input_product_ids_filename = args.input
    search = args.search
    return search, input_product_ids_filename


def main():
    search, input_product_ids_filename = get_script_arguments()
    run(search, input_product_ids_filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
