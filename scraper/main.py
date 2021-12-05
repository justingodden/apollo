from scraper import WfScraper, PageParser


def main():
    scraper = WfScraper()
    scraper.scrape_all_pages()


if __name__ == "__main__":
    main()
