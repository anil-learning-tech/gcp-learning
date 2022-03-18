# author learn_to_smoke_in_clouds

from flask import Flask
app = Flask(__name__)
from flask import  request
import requests
import traceback
gift_card_ip="127.0.0.1"
product_store_ip="127.0.0.1"


@app.route('/healthcheck')
def healthcheck():
    return "front end is healthy"

@app.route('/generate_gift_card')
def generate_gift_card():
    try:
        gift_card_amount = request.args.get("amount")
        customer_id = request.args.get("customer_id")
        input_params={"amount" : gift_card_amount,"customer_id" : customer_id}
        gift_card_service_url="http://{0}:3001/generate_gift_card".format(gift_card_ip)
        print("sending request to generate gift card for  gift card service url {0}".format(gift_card_service_url))
        gift_card_response=requests.get(url = gift_card_service_url, params = input_params)
        return gift_card_response.text
    except Exception as ex:
        print("Exception received in generate gift_card" )
        traceback.print_exc(ex)
        return "error occurred in generate gift card"

@app.route('/get_gift_card')
def get_gift_card():
    try:
        gift_card_no = request.args.get("gift_card_no")
        input_params={"gift_card_no" : gift_card_no}
        gift_card_service_url="http://{0}:3001/get_gift_card".format(gift_card_ip)
        print("sending request to get gift card on server url {0} ".format(gift_card_service_url))
        gift_card_response=requests.get(url = gift_card_service_url, params = input_params)
        return gift_card_response.text
    except Exception as ex:
        print("Exception received in getting gift_card" )
        traceback.print_exc(ex)
        return "error occurred in getting gift card"



@app.route('/buy_products')
def buy_products():
    try:
        products = request.args.get("products")
        gift_card_no = request.args.get("gift_card_no")
        total_amount = request.args.get("total_amount")
        customer_id  = request.args.get("customer_id")
        product_store_url="http://{0}:3002/buy_products".format(product_store_ip)
        print("sending request to buy product on service url {0}".format(product_store_url))
        product_input_params={"products" : products,"gift_card_no":gift_card_no,"total_amount" : total_amount,"customer_id" : customer_id}
        product_transaction_response=requests.get(url = product_store_url, params = product_input_params)
        return product_transaction_response.text
    except Exception as ex:
        print("Exception received in buying product" )
        traceback.print_exc(ex)
        return "error occurred in buying product"


@app.route('/list_all_transactions')
def list_all_transactions():
    try:
        customer_id  = request.args.get("customer_id")
        product_list_all_transaction_url="http://{0}:3002/list_all_transactions".format(product_store_ip)
        print("sending request to get all transaction for url {0}".format(product_list_all_transaction_url))
        product_transaction_response=requests.get(url = product_list_all_transaction_url, params ={"customer_id" : customer_id})
        return product_transaction_response.text
    except Exception as ex:
        print("Exception received in listing all product" )
        traceback.print_exc(ex)
        return "error occurred in listing all product"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3000)