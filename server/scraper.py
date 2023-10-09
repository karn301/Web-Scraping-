import requests
from bs4 import BeautifulSoup
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

