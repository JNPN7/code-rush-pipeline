from selenium_scraper import SeleniumScraper
import argparse

def arg_parser():
    parser = argparse.ArgumentParser(description='Scrape data about the celebrity')
    parser.add_argument('-n', '--name', help="Name of celebrity you want to scrape data about", type=str, required=True)

    args = parser.parse_args()
    return args

def main():
    args = arg_parser()
    scraper = SeleniumScraper()

    celeb_name = args.name
    celeb = scraper.get_celeb_info(celeb_name)
    celeb.store()


if __name__ == "__main__":
    main()
