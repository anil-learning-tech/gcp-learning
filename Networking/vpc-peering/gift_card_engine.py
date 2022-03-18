# author learn_to_smoke_in_clouds

from flask import Flask
app = Flask(__name__)
import psycopg2
from flask import  request
import time

@app.route('/generate_gift_card')
def generate_gift_card():
    gift_card_amount=request.args.get("amount")
    customer_id =request.args.get("customer_id")
    gift_card_number= int(time.time())
    db_generation_query="insert into gift_card_info values (%s,%s,%s) "
    value_list=[customer_id,gift_card_amount,gift_card_number]
    write_in_database(db_generation_query,value_list)
    return "Gift card no {0} generated successfully for customer id {1} with amount {2} ".format(gift_card_number,customer_id,gift_card_amount)

@app.route('/get_gift_card')
def get_existing_gift_card_amount():
    gift_card_no= request.args.get("gift_card_no")
    db_read_query= "select * from gift_card_info where gift_card_no = %s"
    value_list=[gift_card_no]
    gift_card_info=read_from_database(db_read_query,value_list)
    if gift_card_info:
        return {
                "customer_id" : gift_card_info[0][0],
                "amount":gift_card_info[0][1],
                "gift_card_no" :gift_card_info[0][2]
               }
    else:
        return {}

@app.route('/deduct_amount_in_gift_card')
def deduct_amount_in_gift_card():
    gift_card_no= request.args.get("gift_card_no")
    amount_to_be_deducted=request.args.get("amount_to_be_deducted")
    db_query="update gift_card_info  set amount = amount - %s where gift_card_no = %s "
    value_list=[amount_to_be_deducted,gift_card_no]
    write_in_database(db_query,value_list)
    print("amount {0} is deducted for gift card no {1}".format(amount_to_be_deducted,gift_card_no))



@app.route('/has_sufficient_amount')
def has_gift_card_sufficient_amount():
    gift_card_no= request.args.get("gift_card_no")
    amount_to_be_deducted= int(request.args.get("total_amount"))
    db_read_query= "select * from gift_card_info where gift_card_no = %s"
    value_list=[gift_card_no]
    gift_card_info=read_from_database(db_read_query,value_list)
    if gift_card_info:
        amount_present_in_db=int(gift_card_info[0][1])
        if amount_present_in_db >= amount_to_be_deducted:
            return "True"
        else:
            return "False"
    else:
        return "False"


@app.route('/healthcheck')
def healthcheck():
    return "gift card application is healthy"

def create_connection():
    db_connection=psycopg2.connect(database="postgres", user="postgres", password="123456",host="127.0.0.1",port="5432")
    return db_connection

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




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=3001)