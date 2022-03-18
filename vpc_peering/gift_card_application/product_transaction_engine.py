from flask import Flask
app = Flask(__name__)
import psycopg2
from flask import  request
import requests
import time
gift_card_ip="127.0.0.1"


@app.route('/healthcheck')
def healthcheck():
    return "product engine is healthy"

@app.route('/buy_products')
def buy_products():
    products = request.args.get("products")
    gift_card_no = request.args.get("gift_card_no")
    total_amount = request.args.get("total_amount")
    customer_id  = request.args.get("customer_id")
    input_params={"total_amount" : total_amount,"gift_card_no" : gift_card_no,"products" : products}
    gift_card_service_sufficient_amount_url="http://{0}:3001/has_sufficient_amount".format(gift_card_ip)
    print("sending request to gift card service for balance check on url {0} ".format(gift_card_service_sufficient_amount_url))
    gift_card_response=requests.get(url = gift_card_service_sufficient_amount_url, params = input_params)
    has_sufficient_amount=gift_card_response.text
    if has_sufficient_amount=="True":
        transaction_id=int(time.time())
        db_write_query="insert into product_transaction values (%s,%s,%s,%s) "
        value_list=[products,customer_id,total_amount,transaction_id]
        write_in_database(db_write_query,value_list)
        gift_card_service_deduct_amount_url="http://{0}:3001/deduct_amount_in_gift_card".format(gift_card_ip)
        deduct_amount_input_params={"amount_to_be_deducted" : total_amount,"gift_card_no": gift_card_no}
        print("sending request to gift card service to deduct the purchase  amount from gift card on url {0} ".format(gift_card_service_deduct_amount_url))
        gift_card_response=requests.get(url = gift_card_service_deduct_amount_url, params = deduct_amount_input_params)
        return "Product successfully purchased"
    else:
        return "Gift card does not have sufficient balance for transaction"


@app.route('/list_all_transactions')
def list_all_transactions():
    customer_id  = request.args.get("customer_id")
    db_query="select * from product_transaction where customer_id = %s "
    value_list=[customer_id]
    transaction_list=read_from_database(db_query,value_list)
    transaction_ditionary={}
    count=1
    for each_transaction in transaction_list:
        each_formatted_transaction={"products" :each_transaction[0],"customer_id" : each_transaction[1],"total_amount" : each_transaction[2],"transaction_no":each_transaction[3]}
        transaction_ditionary["transaction-"+str(count)] =each_formatted_transaction
        count=count+1
    return transaction_ditionary

def create_connection():
    db_connection=psycopg2.connect(database="postgres", user="postgres", password="123456",host="127.0.0.1",port="5432")
    return db_connection


def write_in_database(query,value_list=None):
    try:
        db_connection=create_connection()
        print("Connection created with database successfully for write operation")
        cursor=db_connection.cursor()
        if value_list is None:
            cursor.execute(query)
        else:
            cursor.execute(query,value_list)
        db_connection.commit()
        print("end of write operation")
    except Exception as ex:
        print("could not connect to database in write operation")
        print(ex)
    finally:
        if (db_connection):
            cursor.close()
            db_connection.close()


def read_from_database(query,value_list=None):
    try:
        connection_for_database=create_connection()
        print("database connected successfully for read operation")
        cursor=connection_for_database.cursor()
        if value_list is None:
            cursor.execute(query)
        else:
            cursor.execute(query,value_list)
        result_from_database=cursor.fetchall()
        return result_from_database
    except Exception as ex:
        print("exception raised while talking to database ")
        print(ex)
    finally:
        if (connection_for_database):
            cursor.close()
            connection_for_database.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port='3002')