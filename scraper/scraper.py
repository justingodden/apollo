from typing import List

import requests
from bs4 import BeautifulSoup
import user_agent

from db_model import Watch


class WfScraper:
    """doc"""

    def __init__(self) -> None:
        self.user_agent = user_agent.generate_user_agent()
        self.URL_ALL_WATCHES = r"https://www.watchfinder.co.uk/all-watches?orderby=BestMatch&pageno="
        self.URL_FIRST_PAGE = r"https://www.watchfinder.co.uk/all-watches?orderby=BestMatch&pageno=1"
        self.URL_BASE = r"https://www.watchfinder.co.uk"
        self.url_list = []

    def get_html(self, url) -> BeautifulSoup:
        req = requests.get(url, headers={"User-Agent": self.user_agent})
        return BeautifulSoup(req.content, "html.parser")

    def get_total_pages(self) -> int:
        soup = self.get_html(self.URL_FIRST_PAGE)
        return int(soup.find("div", {"class": "search_pager"}).find_all("a", {"class": "pager_item"})[-2].text())

    def get_single_page_urls(self, url: str) -> List[str]:
        urls = []
        a_tags = self.get_html(url).find_all('a', {'class': 'prods_name redirect'})
        urls += [self.URL_BASE + a["href"] for a in a_tags]
        return [url.replace(' ', '%20') for url in urls]

    def get_product_url_list(self) -> List[str]:
        total_pages = self.get_total_pages()
        for page in range(1, total_pages+1):
            self.url_list += self.get_single_page_urls(self.URL_ALL_WATCHES + str(page))
        return self.url_list

    def scrape_single_page(self, url: str):
        product_url = url
        soup = self.get_html(url)
        brand = PageParser.parse_brand(soup)
        series = PageParser.parse_series(soup)
        model_num = PageParser.parse_model_num(soup)
        model_id = PageParser.parse_model_id(soup)
        price = PageParser.parse_price(soup)
        year = PageParser.parse_year(soup)
        box = PageParser.parse_box(soup)
        papers = PageParser.parse_papers(soup)
        image_url = PageParser.parse_image_url(soup)
        image_filename = PageParser.parse_image_filename(soup)

    def scrape_all_pages(self):
        self.get_product_url_list()
        for _, url in enumerate(self.url_list):
            self.scrape_single_page(url)


class PageParser:
    """doc"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def parse_brand(soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    def parse_series(soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    def parse_model_num(soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    def parse_model_id(soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    def parse_price(soup: BeautifulSoup) -> int:
        pass

    @staticmethod
    def parse_year(soup: BeautifulSoup) -> int:
        pass

    @staticmethod
    def parse_box(soup: BeautifulSoup) -> bool:
        pass

    @staticmethod
    def parse_papers(soup: BeautifulSoup) -> bool:
        pass

    @staticmethod
    def parse_image_url(soup: BeautifulSoup) -> str:
        pass

    @staticmethod
    def parse_image_filename(soup: BeautifulSoup) -> str:
        pass
