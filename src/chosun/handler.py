import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
import requests
from goose3 import Goose
from goose3.text import StopWordsKorean


# RSS 와 홈페이지에서 파싱하는것을  구별해서 개발
def get_response_page(res: requests.Session(), url):
    try:
        response = res.get(url)
        return response.content.decode('utf-8')
    except:
        return None


def rss(res: requests.Session()):
    rss_url = 'http://myhome.chosun.com/rss/www_section_rss.xml'
    response = get_response_page(res, rss_url)
    html = response.text
    data = feedparser.parse(html)
    for entries in data.entries:
        for link in entries.links:
            new_paper = get_response_page(res, link.href)
            # 기사 원문
            """
            <div class="par"> 
            """
            soup = BeautifulSoup(new_paper, 'html.parser')
            print(soup)
            all_item = soup.find_all("item")
            print(all_item)
            break  # Test 용
        break  # Test 용



# 뉴스 기사 모여있는 page
def paper_route(res: requests.Session()):
    main_page_url = 'https://news.chosun.com/svc/list_in/list.html?catid={}'
    kinds = dict(
        politics='21'  # 정치
    )
    body = get_response_page(res, main_page_url.format(kinds.get('politics')))
    soup = BeautifulSoup(body, 'html.parser')
    all_dl = soup.find('div', {'class': 'list_content'})
    all_news = all_dl.find_all('a')  # 뉴스 기사 url 수집
    for news in all_news:
        'https://news.chosun.com/site/data/html_dir/2020/08/15/2020081500076.html'
        if 'news.chosun.com/site/data/html_dir/' in news.get('href'):
            url = 'https:' + news.get('href')
            news_paper = get_response_page(res, url)
            print(get_title(news_paper))
            print(get_news_create_date(news_paper))
            print(get_body(news_paper))
            break  # Test 용


# 뉴스 제목
def get_title(news_paper: str):
    soup = BeautifulSoup(news_paper, 'html.parser')
    return soup.find('h1', {'id':'news_title_text_id'}).text


# 뉴스 작성일자
def get_news_create_date(news_paper: str):
    soup = BeautifulSoup(news_paper, 'html.parser')
    return soup.find('div', {'class':'news_date'}).text


# 뉴스 본문
def get_body(news_paper):
    soup = BeautifulSoup(news_paper, 'html.parser')
    return soup.find('div', {'class': 'par'}).text





def main():
    with requests.Session() as res:
        # rss(res)
        paper_route(res)


if __name__ == "__main__":
    main()