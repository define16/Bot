import requests
from bs4 import BeautifulSoup
import pandas as pd
import feedparser
import requests
from goose3 import Goose
from goose3.text import StopWordsKorean

# RSS 와 홈페이지에서 파싱하는것을  구별해서 개발
def get_data(url):
    try:
        res = requests.get(url)
        return res.text
    except:
        return None

def rss():
    rss_url = 'http://myhome.chosun.com/rss/www_section_rss.xml'
    with requests.Session() as res:
        response = res.get(rss_url)
        html = response.text
        data = feedparser.parse(html)
        for entries in data.entries:
            for link in entries.links:
                new_paper = get_data(link.href)
                # 기사 원문
                """
                <div class="par"> 
                """
                soup = BeautifulSoup(new_paper, 'html.parser')
                print(soup)
                all_item = soup.find_all("item")
                print(all_item)
                break  # Test
            break  # Test 용


def main():
    rss()


if __name__ == "__main__":
    main()