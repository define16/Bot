import time

from bs4 import BeautifulSoup
from Base import NewspaperDelivery


class HaniHandler(NewspaperDelivery):
    def __init__(self):
        self.news_list = []
        super().__init__()

    def rss(self):
        pass

    def paper_route(self):
        flag = True
        url = "http://h21.hani.co.kr/arti/NEWS?cline={}"
        page = 1
        while flag:
            body = self.get_response_page(url.format(page))
            html = BeautifulSoup(body, 'html.parser')
            all_la = html.find('ul', {'class': 'list_article'})
            all_news = all_la.find_all('div', {'class': 'title1'})
            for news_url in all_news:
                news = "http://h21.hani.co.kr" + news_url.find('a').get('href')  # 뉴스 기사 url 수집
                self.news_list.append(news)

            if not all_news:
                flag = False

            page += 1
            time.sleep(1)

        # TODO 분리할 예정
        for url in self.news_list:
            news_paper = self.get_response_page(url)
            news_paper_html = BeautifulSoup(news_paper, 'html.parser')
            title = self.get_title(news_paper_html)
            registration_time, update_time = self.get_date(news_paper_html)
            body = self.get_body(news_paper_html)
            print("제목 :", title)
            print("생성일 :", registration_time)
            print("수정일 :", update_time)
            print("본문 :", body)

    def get_title(self, html: BeautifulSoup):
        header = html.find('header', {'class': 'article_head'})
        title = header.find('h1').text.strip()
        return title

    def get_date(self, html: BeautifulSoup):
        write_time = html.find('div', {'class': 'datebox'}).text.strip()
        write_time_split = write_time.split(' ')
        registration_time = f'{write_time_split[2]} {write_time_split[3]}'
        update_time = f'{write_time_split[6]} {write_time_split[7]}'

        return registration_time, update_time  # 등록, 변경 시간

    def get_body(self, html: BeautifulSoup):
        header = html.find('div', {'class': 'article_body'})
        header.find('div', {'class': 'together21'}).decompose()  # 각주 삭제
        bodies = header.find_all('div', {'class': 'text'})
        footnote = ''
        body = ''
        for b in bodies:
            if b.text.strip() != '':
                for tag in b.find_all('strong'):
                    footnote = tag.text  # 맨 마지막 strong 태그가 각주
                body += b.text.strip() + ' '

        body = body.replace(footnote, '').strip()  # 각주 제거
        return body
