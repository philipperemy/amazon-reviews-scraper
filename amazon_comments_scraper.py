import argparse
import logging

from core_extract_comments import get_comments_based_on_keyword

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--search')
    args = parser.parse_args()
    DEFAULT_SEARCH = 'BOTANIST ボタニカルシャンプー 490ml ＆ トリートメント 490g　モイストセット'
    search = DEFAULT_SEARCH if args.search is None else args.search
    get_comments_based_on_keyword(search=search)
