import argparse
import logging

from core_generate_product_ids import get_random_product_ids

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    get_random_product_ids()
    # main()
