import argparse
import logging

from core_generate_product_ids import get_random_product_ids

DEFAULT_OUTPUT_FILENAME = 'product_ids.txt'

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    output = DEFAULT_OUTPUT_FILENAME if args.output is None else args.output
    get_random_product_ids(output)
