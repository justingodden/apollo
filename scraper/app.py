from scraper import WfScraper


def handler(event, context):
    scraper = WfScraper()
    scraper.scrape_all_pages()
