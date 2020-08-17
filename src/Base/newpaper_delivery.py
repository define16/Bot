from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from requests import Session


class NewspaperDelivery(ABC):
    def __init__(self):
        self.request = Session()

    def get_response_page(self, url):
        response = self.request.get(url)
        try:
            return response.content.decode('utf-8')
        except UnicodeDecodeError:
            return response.content

    @abstractmethod
    def rss(self):
        pass

    # 뉴스 기사 모여있는 page
    @abstractmethod
    def paper_route(self):
        pass

    # 뉴스 제목
    @abstractmethod
    def get_title(self, html: BeautifulSoup):
        return html.find('h1', {'id': 'news_title_text_id'}).text

    # 뉴스 작성일자
    @abstractmethod
    def get_date(self, html: BeautifulSoup):
        return html.find('div', {'class': 'news_date'}).text

    # 뉴스 본문
    @abstractmethod
    def get_body(self, html: BeautifulSoup):
        return html.find('div', {'class': 'par'}).text