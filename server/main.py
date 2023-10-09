
import requests
import scraper as sp
from flask import Flask, json, request
from transformers import pipeline
from bs4 import BeautifulSoup
nlp = pipeline('question-answering', model='deepset/roberta-base-squad2', tokenizer='deepset/roberta-base-squad2')

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






app = Flask(__name__)



# Define your route here
@app.route("/home", methods=["GET", "POST"])
def home():
    return "Hello, Welcome to home."


@app.route("/getBasicData", methods=["POST"])
def getBasicDataRoute():
    body = request.get_json()
    print(body)
    text = sp.getBasicData(soup=soup)
    nlp({
        'question': body['question'],
        "context": text 
    })

    response = app.response_class(
        response = json.dumps({
            "status" : 200,
            "message" : nlp['answer']
        })
    )

    return response
    

@app.route("/questionAsk", methods=["POST"])
def questionAsk():

    response = app.response_class(
        response = json.dumps({
        "Hello" : "Hello Word"
    }),
    mimetype="application/json"
    )


    return response





if __name__ == "__main__":
    app.run()
    