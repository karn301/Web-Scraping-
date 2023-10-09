from flask import Flask, json
from transformers import pipeline
nlp = pipeline('question-answering', model='deepset/roberta-base-squad2', tokenizer='deepset/roberta-base-squad2')

app = Flask(__name__)

context = """The name of the product is Crucial RAM 8GB DDR4 3200MHz CL22 (or 2933MHz or 2666MHz) Laptop Memory CT8G4SFRA32A . 
It's Price is 1,499.Some specific details are as Brand is Crucial,Computer Memory Size is 8 GB, RAM Memory Technology is DDR4 ,Memory Speed is 3200 MHz, 
Compatible Devices is Laptop, Features are  Improve your system's responsiveness, run apps faster and multitask with ease. Extended timings - 22-22-22 
Install with ease; no computer skills required How-to guides available at Crucial   Compatibility assurance when using the Crucial System Scanner or C
rucial Advisor Tool   Micron quality and reliability is backed by superior component and module level testing and 42 years of memory expertise  
ECC Type Non-ECC, Form Factor SODIMM, Pin Count 260-pin, PC Speed PC4-25600, Voltage 12V, Rank and Configuration 1Rx16, 1Rx8 or 2Rx8.NOTE: 
DRAM modules require configuration to specific systems  .Can be deliveredFREE delivery Wednesday, 11 October..Fastest Delivery by Fastest delivery tomorrow, 
9 october. order within 19 hrs 55 mins..Stock Availablity = In stock.Seller information Sold by Appario Retail Private Ltd and Fulfilled by Amazon."""



# Define your route here
@app.route("/home", methods=["GET", "POST"])
def home():
    return "Hello, Welcome to home."

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
    