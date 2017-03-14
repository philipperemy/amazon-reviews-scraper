import argparse

from core_extract_comments import *
from core_utils import persist_comment_to_disk

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    input_product_ids_filename = args.input

    if input_product_ids_filename is not None:
        with open(input_product_ids_filename, 'r') as r:
            product_ids = [p.strip() for p in r.readlines()]
            print('{} product ids were found.'.format(len(product_ids)))
            for product_id in product_ids:
                reviews = get_comments_with_product_id(product_id)
                for review in reviews:
                    persist_comment_to_disk(review)
    else:
        DEFAULT_SEARCH = 'BOTANIST ボタニカルシャンプー 490ml ＆ トリートメント 490g　モイストセット'
        search = DEFAULT_SEARCH if args.search is None else args.search
        reviews = get_comments_based_on_keyword(search=search)
        for review in reviews:
            persist_comment_to_disk(review)
