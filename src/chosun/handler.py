import time
from bs4 import BeautifulSoup
import feedparser

from Base import NewspaperDelivery


class ChosunHandler(NewspaperDelivery):
    def rss(self):
        rss_url = 'http://myhome.chosun.com/rss/www_section_rss.xml'
        response = self.get_response_page(rss_url)
        html = response.text
        data = feedparser.parse(html)
        for entries in data.entries:
            for link in entries.links:
                new_paper = self.get_response_page(link.href)
                # 기사 원문
                """
                <div class="par"> 
                """
                soup = BeautifulSoup(new_paper, 'html.parser')
                all_item = soup.find_all("item")
                print(soup)
                print(all_item)
                break  # Test 용
            break  # Test 용

    # 뉴스 기사 모여있는 page
    def paper_route(self):
        flag = True
        page = 1
        main_page_url = 'https://news.chosun.com/svc/list_in/list.html?catid={}&pn={}'
        kinds = dict(
            politics='21'  # 정치
        )
        while flag:
            body = self.get_response_page(main_page_url.format(kinds.get('politics'), page))
            html = BeautifulSoup(body, 'html.parser')
            all_dl = html.find('div', {'class': 'list_content'})
            all_news = all_dl.find_all('a')  # 뉴스 기사 url 수집
            for news in all_news:
                # 신문 본문 페이지 URL
                if 'news.chosun.com/site/data/html_dir/' in news.get('href'):
                    url = 'https:' + news.get('href')
                    news_paper = self.get_response_page(url)
                    news_paper_html = BeautifulSoup(news_paper, 'html.parser')
                    title = self.get_title(news_paper_html)
                    news_date = self.get_date(news_paper_html)
                    body = self.get_body(news_paper_html)
                    print(title)
                    print(news_date)
                    print(body)
                    # Queue로 전달 후 저장
                else:
                    pass

            if not all_news:
                flag = False

            page += 1
            time.sleep(1)

    # 뉴스 제목
    def get_title(self, html: BeautifulSoup):
        return html.find('h1', {'id': 'news_title_text_id'}).text

    # 뉴스 작성일자
    def get_date(self, html: BeautifulSoup):
        return html.find('div', {'class': 'news_date'}).text

    # 뉴스 본문
    def get_body(self, html: BeautifulSoup):
        return html.find('div', {'class': 'par'}).text
