# analysis on jumia pdts feedback reviews

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

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
    except ValueError:
        print("unkonwn url")

# pdt_url = "https://www.jumia.co.ke/generic-colorscreen-smartwatch-heart-rate-sport-bracelet-152366245.html"
# pdt_url = "https://www.jumia.co.ke/itel-isw-o11-sones-smart-watch-native-storm-215779600.html"
# pdt_url = "https://www.jumia.co.ke/nexus-nx-ir-dst-electric-dry-steam-iron-box-1300w-green-3yrs-wrty-169322250.html"
# pdt_url = "https://www.jumia.co.ke/hp-27f-display-27-ultra-slim-ips-full-hd32gb-flash-39312361.html"
pdt_url = "https://www.jumia.co.ke/generic-6in1-10-inch-ring-light2.1m-tripod-stand-for-tiktok-youtube-giftmicremote-159690042.html"
pdt_html = get_html(pdt_url)

def get_feedback_url(html):
    # gets the url to a specified product feedback page
    # accepts html
    soup = BeautifulSoup(html, 'html.parser')
    feed_back_section = soup.find('a', class_='btn _def _ti -mhs -fsh0')
    feed_back_anchor = feed_back_section.get('href')
    feedback_page_url = BASE_URL + feed_back_anchor
    return feedback_page_url

print(get_feedback_url(pdt_html))

feed_back_url = get_feedback_url(pdt_html)

feedback_html = get_html(feed_back_url)

# feedback_html = get_feedback_url(pdt_html)

soup2 = BeautifulSoup(feedback_html, 'html.parser')
reviews = soup2.find_all('article', class_="-pvs -hr _bet")
# print(reviews)
# for review in reviews:
#     print("rating : ", review.find('div', class_="stars _m _al -mvs").get_text())
#     print("title : ", review.find('h3', class_="-m -fs16 -pvs").get_text())
#     print("review : ", review.find('p', class_="-pvs").get_text())
#     print("date : ", review.find('span', class_="-prs").get_text())
#     print("by : ", review.find('div', class_="-pvs").get_text())
#     print("verified : ", review.find('div', class_="-df -i-ctr -gn5 -fsh0").get_text())
#     print()


reviews = soup2.find_all('article', class_="-pvs -hr _bet")
# print(reviews)
ratings = list()
titles = list()
reviews_ = list()
date_ = list()
reviewed_by = list()
verified_purchaser = list()
for review in reviews:
    rating = review.find('div', class_="stars _m _al -mvs").get_text()
    ratings.append(rating)
    title = review.find('h3', class_="-m -fs16 -pvs").get_text()
    titles.append(title)
    rev = review.find('p', class_="-pvs").get_text()
    reviews_.append(rev)
    date = review.find('span', class_="-prs").get_text()
    date_.append(date)
    by = review.find('div', class_="-pvs").get_text()
    reviewed_by.append(by)
    verified = review.find('div', class_="-df -i-ctr -gn5 -fsh0").get_text()
    verified_purchaser.append(verified)

# for pandas
import pandas as pd
data = {
    'ratings' : ratings,
    'title' : titles,
    'review' : reviews_,
    'date' : date_,
    'reviewd_by' : reviewed_by
}

my_d = pd.DataFrame(data)
my_d.to_csv('test.csv')