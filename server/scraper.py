import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver



url ="""https://www.amazon.in/Crucial-3200MHz-2933MHz-2666MHz-CT8G4SFRA32A/dp/B08C4Z69LN/?_encoding=UTF8&pd_rd_w=asRZX&content-id=amzn1.sym.aff93425-4e25-4d86-babd-0fa9faf7ca5d%3Aamzn1.symc.36bd837a-d66d-47d1-8457-ffe9a9f3ddab&pf_rd_p=aff93425-4e25-4d86-babd-0fa9faf7ca5d&pf_rd_r=3S93CHJY45SQRCD4R7DC&pd_rd_wg=d59M2&pd_rd_r=ae6fcfa5-1b50-4c83-a0ee-f2a9eb1e8361&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1"""

headers = {'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}
# get url result html code here 
page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')


frog = soup.text

# Summarizer Url
summarize_endpoint = url.replace("/dp/","/product-reviews/")+f"?pageNumber={1}"

# Critical Review
critical_review = url.replace("/dp/","/product-reviews/")+"&filterByStar=critical"

# Positive Review
positive_review = url.replace("/dp/","/product-reviews/")+"&filterByStar=positive"


def getTablesToObj(soup:BeautifulSoup):
    obj_table = []
    table = soup.find('table', class_="a-normal a-spacing-micro")
    rows = table.find_all("tr")

    for row in rows:
        key = row.find_all("span")[0].text
        value = row.find_all("span")[1].text

        obj = {
            key : value
        }

        obj_table.append(obj)
    return obj_table


#customer reviews for summarization

def extractReviews(summarizer_url):
    resp = requests.get(summarizer_url)
    review_soup = BeautifulSoup(resp.text,'html.parser')
    reviews = review_soup.findAll('div',{'data-hook':'review'})
    review=""
    for item in reviews:
        if len(item.find('span',{'data-hook':'review-body'}).text.strip()) < 10:
            continue
        review += item.find('span',{'data-hook':'review-body'}).text.strip()
    return review


# Top review
def topReview(url):
    crit_review_list = []
    resp = requests.get(url)
    review_soup = BeautifulSoup(resp.text,'html.parser')
    reviews = review_soup.findAll('div',{'data-hook':'review'})
    for item in reviews:
            review={
                'Rating':item.find('i',{'data-hook':'review-star-rating'}).text.strip()[:3],
                'Review Body':item.find('span',{'data-hook':'review-body'}).text.strip(),
            }
            crit_review_list.append(review)
            break


def getCriticalAndPositiveCount(positive, critical):
    resp1 = requests.get(critical)
    soup1 = BeautifulSoup(resp1.text,'html.parser')
    resp2 = requests.get(positive)
    soup2 = BeautifulSoup(resp2.text,'html.parser')

    reviews_no1 = soup1.find('div',{'data-hook':'cr-filter-info-review-rating-count'})
    reviews_no2 = soup2.find('div',{'data-hook':'cr-filter-info-review-rating-count'})
    
    crit_count = int(reviews_no1.text.strip().split(', ')[1].split(" ")[0].replace(",",""))
    pos_count = int(reviews_no2.text.strip().split(', ')[1].split(" ")[0].replace(",",""))

    pos_count_per = (100*pos_count)/(pos_count+crit_count)
    crit_count_per = (100*crit_count)/(pos_count+crit_count)

    return [pos_count_per, crit_count_per]



def getBasicData(soup: BeautifulSoup):

    # title here
    title = soup.find('span', id="productTitle").text
    title = re.sub(r'\s+'," ",title)

    # For price
    price = str(soup.find("span", class_='a-price-whole').text).replace(".", "")

    # Features here
    list_ =  soup.find("div", id="feature-bullets").find_all('li')
    features = [i.text for i in list_]
    
    # Get your table into object list here
    table = getTablesToObj(soup=soup)

    features_text = ""
    for ele in features:
            features_text += ele

    table_result = ""
    for item in table:
        key, value = list(item.items())[0]
        table_result += f'{key} is {value}.'

    # Delivery details
    delivery = soup.find('div',id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE")
    delivery = delivery.text.strip().removesuffix('Details').strip()

    # Fastest Delivery
    fast_delivery = soup.find('div',id="mir-layout-DELIVERY_BLOCK-slot-SECONDARY_DELIVERY_MESSAGE_LARGE")
    fast_delivery = fast_delivery.text.strip().removesuffix('Details').removeprefix('Or').strip().capitalize()

    #availability
    availability = soup.find('div', id="availability").text.strip()

    # seller info
    seller_information = soup.find('div', id = "merchant-info").text.strip()

    # chunks for  title, features, table, seller, delivery, Availability
    text = 'Title and Brand of the product is '+title+'.'+'Price of the product is ₹'+ price+'.'+'Some specific details about the product are as'+table_result+'.'+'Features are '+features_text+'.'+'Can be delivered by '+delivery+'.'+'Fastest Delivery by '+fast_delivery+'.'+'Stock Availablity '+availability+'.'+'Seller information '+seller_information

    driver = webdriver.Chrome()
    driver.get("https://www.paraphraser.io/")
    input_box = driver.find_element('id',"input-content")
    input_box.send_keys(text)
    submit_button = driver.find_element('id',"paraphrase_now")
    submit_button.click()
    result_element = driver.find_element('id',"output-content")
    result_data = result_element.text
    driver.quit()
    
    
    return result_data