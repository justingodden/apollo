from scraper import WfScraper, PageParser


def main():
    scraper = WfScraper()
    parser = PageParser()
    # return scraper.get_product_url_list()
    url = "https://www.watchfinder.co.uk/Tag%20Heuer/Carrera/CAR2A1Z.FT6044/29627/item/204357"
    return parser.parse_box(scraper.get_html(url))


if __name__ == "__main__":
    print(main())
