from typing import List
import os
import re

import requests
from bs4 import BeautifulSoup
import pandas as pd
import user_agent

from db_model import Watch, add_to_db, create_db_and_tables, url_exists_in_db


class WfScraper:
    """doc"""

    def __init__(self) -> None:
        self.user_agent = user_agent.generate_user_agent()
        self.URL_ALL_WATCHES = r"https://www.watchfinder.co.uk/all-watches?orderby=BestMatch&pageno="
        self.URL_FIRST_PAGE = r"https://www.watchfinder.co.uk/all-watches?orderby=BestMatch&pageno=1"
        self.URL_BASE = r"https://www.watchfinder.co.uk"
        self.url_list = []
        create_db_and_tables()

    def get_html(self, url) -> BeautifulSoup:
        req = requests.get(url, headers={"User-Agent": self.user_agent})
        return BeautifulSoup(req.content, "html.parser")

    def get_total_pages(self) -> int:
        soup = self.get_html(self.URL_FIRST_PAGE)
        return int(soup.find("div", {"class": "search_pager"}).
                   find_all("a", {"class": "pager_item"})[-2].get_text())

    def get_single_page_urls(self, url: str) -> List[str]:
        urls = []
        a_tags = self.get_html(url).find_all('a', {'class': 'prods_name redirect'})
        urls += [self.URL_BASE + a["href"] for a in a_tags]
        return [url.replace(' ', '%20') for url in urls]

    def get_product_url_list(self) -> List[str]:
        print("Generating url list.")
        total_pages = self.get_total_pages()
        for page in range(1, total_pages+1):
            self.url_list += self.get_single_page_urls(self.URL_ALL_WATCHES + str(page))
            print(f"{page}/{total_pages} url pages scraped...", end="\r")
        return self.url_list

    def scrape_single_page(self, url: str) -> None:
        if not url_exists_in_db(url):
            try:
                watch = Watch()
                soup = self.get_html(url)
                watch.product_url = url
                watch.model_id = url.split('/')[-3]
                watch.brand = PageParser.parse_brand(soup)
                watch.series = PageParser.parse_series(soup)
                watch.model_num = PageParser.parse_model_num(soup)
                watch.price = PageParser.parse_price(soup)
                watch.year = PageParser.parse_year(soup)
                watch.box = PageParser.parse_box(soup)
                watch.papers = PageParser.parse_papers(soup)
                watch.image_url = PageParser.parse_image_url(soup)
                watch.image_filename = PageParser.parse_image_filename(soup)
                add_to_db(watch)
            except Exception as e:
                print()
                print(e)

    def scrape_all_pages(self) -> None:
        self.get_product_url_list()
        print("\nScraping all product pages.")
        for i, url in enumerate(self.url_list):
            self.scrape_single_page(url)
            print(f"{i+1}/{len(self.url_list)} products scraped...", end="\r")


class PageParser:
    """doc"""

    def __init__(self) -> None:
        pass

    @staticmethod
    def parse_brand(soup: BeautifulSoup) -> str:
        return soup.find("span", {"class": "prod_brand"}).get_text()

    @staticmethod
    def parse_series(soup: BeautifulSoup) -> str:
        return soup.find("span", {"class": "prod_series"}).get_text()

    @staticmethod
    def parse_model_num(soup: BeautifulSoup) -> str:
        return soup.find("span", {"class": "prod_model"}).get_text()

    @staticmethod
    def parse_price(soup: BeautifulSoup) -> float:
        return float(soup.find("meta", {"itemprop": "price"})["content"])

    @staticmethod
    def parse_year(soup: BeautifulSoup) -> int:
        year = PageParser._parse_table(soup).loc["Year"].values[0]
        return int(re.sub(r"[^0-9]", "", year))

    @staticmethod
    def parse_box(soup: BeautifulSoup) -> bool:
        box = PageParser._parse_table(soup).loc["Box"].values[0]
        return True if box == "Yes" else False

    @staticmethod
    def parse_papers(soup: BeautifulSoup) -> bool:
        papers = PageParser._parse_table(soup).loc["Papers"].values[0]
        return True if papers == "Yes" else False

    @staticmethod
    def parse_image_url(soup: BeautifulSoup) -> str:
        return soup.find("meta", {"itemprop": "image"})["content"]

    @staticmethod
    def parse_image_filename(soup: BeautifulSoup) -> str:
        return os.path.basename(soup.find("meta", {"itemprop": "image"})["content"])

    @staticmethod
    def _parse_table(soup: BeautifulSoup) -> pd.DataFrame:
        table = str(soup.find("table", {"class": "prod_info-table"}))
        return pd.read_html(table)[0].set_index(0, drop=True)
