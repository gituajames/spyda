# analysis on jumia pdts feedback reviews

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request, URLError
import re

BASE_URL = 'https://jumia.co.ke'

def get_html(url):

    # opens specified urls and returns html that can be parsed

    my_request = Request(
        url = url,
        headers = {'User-Agent' : 'Mozilla/5.0'}
    )

    try:
        page = urlopen(my_request)
        html_bytes = page.read()
        html = html_bytes.decode()
        return html
    except URLError:
        print("name or service not known")



def get_feedback_url(html):
    # gets the url to a specified product feedback page
    # accepts html
    soup = BeautifulSoup(html, 'html.parser')
    feed_back_section = soup.find('a', class_='btn _def _ti -mhs -fsh0')
    feed_back_anchor = feed_back_section.get('href')
    feedback_page_url = BASE_URL + feed_back_anchor
    return feedback_page_url

# many_reviews_urls = 'https://www.jumia.co.ke/freeyond-m58gb128gb6.52-50mp4g-smartphone-5000mah-dual-sim-android-phoneblack-109530226.html'
many_reviews_urls = 'https://www.jumia.co.ke/tecno-pop-7-6.6-hd-2gb-64gb-8mp-4g-dual-sim-5000mah-endless-black-1yr-wrty-123170181.html'
no_reviews_url = 'https://www.jumia.co.ke/generic-beitian-high-precision-glonass-bds-galileo-gps-antenna-waterproof-gnss-rtk-board-receiver-antenna-bt-300-model-multi-frequency-antenna-166227973.html'

my_pdt_html = get_html(many_reviews_urls)
my_pdt_feedback_url = get_feedback_url(my_pdt_html)
my_pdt_html_page = get_html(my_pdt_feedback_url)
soup2 = BeautifulSoup(my_pdt_html_page, 'html.parser')


def get_all_urls(soup_object):
    # takes in a soup object and returns a list of all urls with reviews
    url_list = list()
    my_regex = r'([page=]\d+)'
    pages = '?page='
    all_review_pages = soup_object.find("a", attrs={"aria-label": "Last Page"})
    match = re.search(my_regex, all_review_pages.get('href'))
    final_page = match.group(0).strip('=')
    for i in range(1, int(final_page)+1):
        url = get_feedback_url(my_pdt_html)+pages+str(i)
        url_list.append(url)
    return url_list
print(get_all_urls(soup2)) 


all_url_list = get_all_urls(soup2)

ratings = list()
titles = list()
reviews_ = list()
date_ = list()
reviewed_by = list()
verified_purchaser = list()

for url in all_url_list:
    my_pdt_html_page = get_html(url)
    soup3 = BeautifulSoup(my_pdt_html_page, 'html.parser')

    reviews = soup3.find_all('article', class_="-pvs -hr _bet")
    # print(reviews)
    
    for review in reviews:
        # print("rating : ", review.find('div', class_="stars _m _al -mvs").get_text())
        rating = review.find('div', class_="stars _m _al -mvs").get_text()
        ratings.append(rating)
        # print("title : ", review.find('h3', class_="-m -fs16 -pvs").get_text())
        title = review.find('h3', class_="-m -fs16 -pvs").get_text()
        titles.append(title)
        # print("review : ", review.find('p', class_="-pvs").get_text())
        rev = review.find('p', class_="-pvs").get_text()
        reviews_.append(rev)
        # print("date : ", review.find('span', class_="-prs").get_text())
        date = review.find('span', class_="-prs").get_text()
        date_.append(date)
        # print("by : ", review.find('div', class_="-pvs").get_text())
        by = review.find('div', class_="-pvs").get_text()
        reviewed_by.append(by)
        # print("verified : ", review.find('div', class_="-df -i-ctr -gn5 -fsh0").get_text())
        verified = review.find('div', class_="-df -i-ctr -gn5 -fsh0").get_text()
        verified_purchaser.append(verified)
    # print(ratings)
print(len(ratings))
print(len(titles))
print(len(reviews_))
print(len(date_))
print(len(reviewed_by))

import pandas as pd
data = {
    'ratings' : ratings,
    'title' : titles,
    'review' : reviews_,
    'date' : date_,
    'reviewd_by' : reviewed_by
}

my_d = pd.DataFrame(data)
my_d.head()

my_d.to_csv('script_test.csv')