from expressvpn import wrapper

from amazon_comments_scraper import *
from banned_exception import BannedException


def main():
    search, input_product_ids_filename = get_script_arguments()
    while True:
        try:
            run(search, input_product_ids_filename)
        except BannedException as be:
            logging.info('EXCEPTION CAUGHT in __MAIN__')
            logging.info(be)
            logging.info('Lets change our PUBLIC IP GUYS!')
            change_ip()
        except Exception as e:
            logging.error('Exception raised')
            logging.error(e)


def change_ip():
    max_attempts = 10
    attempts = 0
    while True:
        attempts += 1
        try:
            logging.info('GETTING NEW IP')
            wrapper.random_connect()
            logging.info('SUCCESS')
            return
        except Exception as e:
            if attempts > max_attempts:
                logging.error('Max attempts reached for VPN. Check its configuration.')
                logging.error('Browse https://github.com/philipperemy/expressvpn-python.')
                logging.error('Program will exit.')
                exit(1)
            logging.error(e)
            logging.error('Skipping exception.')


if __name__ == '__main__':
    main()
