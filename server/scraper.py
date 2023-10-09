import requests
from bs4 import BeautifulSoup
import re




url ="""https://www.amazon.in/Crucial-3200MHz-2933MHz-2666MHz-CT8G4SFRA32A/dp/B08C4Z69LN/?_encoding=UTF8&pd_rd_w=asRZX&content-id=amzn1.sym.aff93425-4e25-4d86-babd-0fa9faf7ca5d%3Aamzn1.symc.36bd837a-d66d-47d1-8457-ffe9a9f3ddab&pf_rd_p=aff93425-4e25-4d86-babd-0fa9faf7ca5d&pf_rd_r=3S93CHJY45SQRCD4R7DC&pd_rd_wg=d59M2&pd_rd_r=ae6fcfa5-1b50-4c83-a0ee-f2a9eb1e8361&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1"""
# url ="""https://www.amazon.in/Crucial-3200MHz-2933MHz-2666MHz-CT8G4SFRA32A/dp/B08C4Z69LN/?_encoding=UTF8&pd_rd_w=asRZX&content-id=amzn1.sym.aff93425-4e25-4d86-babd-0fa9faf7ca5d%3Aamzn1.symc.36bd837a-d66d-47d1-8457-ffe9a9f3ddab&pf_rd_p=aff93425-4e25-4d86-babd-0fa9faf7ca5d&pf_rd_r=3S93CHJY45SQRCD4R7DC&pd_rd_wg=d59M2&pd_rd_r=ae6fcfa5-1b50-4c83-a0ee-f2a9eb1e8361&ref_=pd_gw_ci_mcx_mr_hp_atf_m&th=1"""
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
# "Accept-Encoding": "gzip, deflate, br"}

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

# testing demo site here
# page = open('index.html', 'r')

# display the data
print(page.content)



soup = BeautifulSoup(page.content, 'html.parser')
# soup = BeautifulSoup(page.read(), 'html.parser')
frog = soup.text

# get all the product details here

# title here
title = soup.find('span', id="productTitle").text
title = re.sub(r'\s+'," ",title)

# For price
price = str(soup.find("span", class_='a-price-whole').text).replace(".", "")

# Features here
list_ =  soup.find("div", id="feature-bullets").find_all('li')
features = [i.text for i in list_]

def getTablesToObj():
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


# Get your table into object list here
table = getTablesToObj()




features_text = ""
for ele in features:
        features_text += ele
features_text




table_result = ""
for item in table:
    key, value = list(item.items())[0]
    table_result += f'{key} is {value}.'
print(table_result)




# Delivery details
delivery = soup.find('div',id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE")
delivery = delivery.text.strip().removesuffix('Details').strip()



# Fastest Delivery
fast_delivery = soup.find('div',id="mir-layout-DELIVERY_BLOCK-slot-SECONDARY_DELIVERY_MESSAGE_LARGE")
fast_delivery = fast_delivery.text.strip().removesuffix('Details').removeprefix('Or').strip().capitalize()



#availability
availability = soup.find('div', id="availability").text.strip()
availability


# seller info
seller_information = soup.find('div', id = "merchant-info").text.strip()
seller_information


# chunks for  title, features, table, seller, delivery, Availability
text = 'Title and Brand of the product is '+title+'.'+'Price of the product is ₹'+ price+'.'+'Some specific details about the product are as'+table_result+'.'+'Features are '+features_text+'.'+'Can be delivered by '+delivery+'.'+'Fastest Delivery by '+fast_delivery+'.'+'Stock Availablity '+availability+'.'+'Seller information '+seller_information
	
text
from selenium import webdriver
# Replace 'path_to_chromedriver' with the actual path to your ChromeDriver executable

driver = webdriver.Chrome()
driver.get("https://www.paraphraser.io/")
input_box = driver.find_element('id',"input-content")
input_box.send_keys(text)
submit_button = driver.find_element('id',"paraphrase_now")
submit_button.click()
result_element = driver.find_element('id',"output-content")
result_data = result_element.text
driver.quit()
result_data




#customer reviews for summarization

import pandas as pd
def extractReviews(review_url):
    resp = requests.get(review_url)
    review_soup = BeautifulSoup(resp.text,'html.parser')
    reviews = review_soup.findAll('div',{'data-hook':'review'})
    review=""
    for item in reviews:
        if len(item.find('span',{'data-hook':'review-body'}).text.strip()) < 10:
            continue
        review += item.find('span',{'data-hook':'review-body'}).text.strip()
    return review


review_url = url.replace("/dp/","/product-reviews/")+f"?pageNumber={1}"
# nPages = totalPages(review_url)
# extractReviews(review_url)
final_res=""
for i in range(1):
    try:
        review_url = url.replace("/dp/","/product-reviews/")+f"?pageNumber={i}"
        final_res += extractReviews(review_url)
    except Exception as e:
        print(e)
final_res




# Top Critical review
crit_review_list = []
def topCriticalReview(review_url_crit):
    resp = requests.get(review_url_crit)
    crit_review_soup = BeautifulSoup(resp.text,'html.parser')
    crit_reviews = crit_review_soup.findAll('div',{'data-hook':'review'})
    for item in crit_reviews:
            review={
                'Rating':item.find('i',{'data-hook':'review-star-rating'}).text.strip()[:3],
                'Review Body':item.find('span',{'data-hook':'review-body'}).text.strip(),
            }
            crit_review_list.append(review)
            break
review_url_crit = url.replace("/dp/","/product-reviews/")+"&filterByStar=critical"
topCriticalReview(review_url_crit)
df = pd.DataFrame(crit_review_list)
df





# Critical review summarization

def CriticalReview(review_url_crit):
    resp = requests.get(review_url_crit)
    crit_review_soup = BeautifulSoup(resp.text,'html.parser')
    crit_reviews = crit_review_soup.findAll('div',{'data-hook':'review'})
    review=""
    for item in crit_reviews:
        if len(item.find('span',{'data-hook':'review-body'}).text.strip()) < 10:
            continue
        review += item.find('span',{'data-hook':'review-body'}).text.strip()
    return review
review_url = url.replace("/dp/","/product-reviews/")+"&filterByStar=critical"
print(review_url)
final_res=""
for i in range(1):
    try:
        review_url = url.replace("/dp/","/product-reviews/")+"&filterByStar=critical"
        final_res += CriticalReview(review_url)
    except Exception as e:
        print(e)
final_res



# Positive review summarization

def PositiveReview(review_url_crit):
    resp = requests.get(review_url_crit)
    pos_review_soup = BeautifulSoup(resp.text,'html.parser')
    pos_reviews = pos_review_soup.findAll('div',{'data-hook':'review'})
    review=""
    for item in pos_reviews:
        if len(item.find('span',{'data-hook':'review-body'}).text.strip()) < 10:
            continue
        review += item.find('span',{'data-hook':'review-body'}).text.strip()
    return review
review_url = url.replace("/dp/","/product-reviews/")+"&filterByStar=positive"
print(review_url)
final_res=""
for i in range(1):
    try:
        review_url = url.replace("/dp/","/product-reviews/")+"&filterByStar=positive"
        final_res += PositiveReview(review_url)
    except Exception as e:
        print(e)
final_res



# Top positive review
pos_review_list = []
def topPositiveReview(review_url_pos):
    resp = requests.get(review_url_pos)
    pos_review_soup = BeautifulSoup(resp.text,'html.parser')
    pos_reviews = pos_review_soup.findAll('div',{'data-hook':'review'})
    for item in pos_reviews:
            review={
                'Review Title':item.find('a',{'data-hook':'review-title'}).text.strip()[19:],
                'Rating':item.find('i',{'data-hook':'review-star-rating'}).text.strip()[:3],
                'Review Body':item.find('span',{'data-hook':'review-body'}).text.strip(),
            }
            pos_review_list.append(review)
            break
review_url_pos = url.replace("/dp/","/product-reviews/")+"filterByStar=positive"
topPositiveReview(review_url_pos)
df = pd.DataFrame(pos_review_list)
df



# Ratings percentage
review_url_crit_count = url.replace("/dp/","/product-reviews/")+"&filterByStar=critical"
review_url_pos_count = url.replace("/dp/","/product-reviews/")+"&filterByStar=positive"

resp1 = requests.get(review_url_crit_count)
soup1 = BeautifulSoup(resp1.text,'html.parser')
resp2 = requests.get(review_url_pos_count)
soup2 = BeautifulSoup(resp2.text,'html.parser')
reviews_no1 = soup1.find('div',{'data-hook':'cr-filter-info-review-rating-count'})
reviews_no2 = soup2.find('div',{'data-hook':'cr-filter-info-review-rating-count'})
crit_count = int(reviews_no1.text.strip().split(', ')[1].split(" ")[0].replace(",",""))
pos_count = int(reviews_no2.text.strip().split(', ')[1].split(" ")[0].replace(",",""))
pos_count_per = (100*pos_count)/(pos_count+crit_count)
print(round(pos_count_per,2))
crit_count_per = (100*crit_count)/(pos_count+crit_count)
print(round(crit_count_per,2))