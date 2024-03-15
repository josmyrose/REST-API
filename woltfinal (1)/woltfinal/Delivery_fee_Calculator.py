#Import necessary libraries
from flask import request, jsonify
from flask_restful import Resource
import math
import pytz #to work with time zones
from datetime import datetime

class Delivery_fee_Calculator(Resource):
    def __init__(self):
        '''
         To initialize the instance attributes
        '''
        self.cart_value =request.json["cart_value"]
        self.delivery_distance =request.json["delivery_distance"]
        self.number_of_items =request.json["number_of_items"]
        self.delivery_time = datetime.strptime(request.json["time"],"%Y-%m-%dT%H:%M:%S%z")
        self.delivery_fee = 0 #Initialize the delivery fee is 0

        
    def cart_Value_Surcharge(self):
        '''
        Calculate surcharge based on th cart value and add surcharge to delivery fee
        max() method is used to find the surcharge
        '''
        surcharge=round(max(0,1000-self.cart_value),2)
        self.delivery_fee+=surcharge

    def distance_Delivery(self):
        '''
        Calculate delivery fee based on the distance and 
        '''
        if self.delivery_distance<=1000:  #If delivery distance is <=1000 ,delivery fee is 200 cents.
            self.delivery_fee+=200
        else:
            self.delivery_fee+=200+((math.ceil(self.delivery_distance/500)-2)*100)
        
    def no_Of_Items_Delivery(self):
        '''
        Calculate surcharge based on number of items and add surcharge to delivery fee.
        '''
        surcharge=0
        if self.number_of_items < 13:
         surcharge+=max(0,self.number_of_items-4)*50
        else:
            surcharge+=((self.number_of_items-4)*50)+120
        self.delivery_fee+=surcharge

    def delivery_Fee_Limit(self):
        '''
        Limit the delivery fee can never be exceed 1500 cent including possible surcharge.
        '''
        self.delivery_fee=min(1500,self.delivery_fee)

    def delivery_Fee_Free (self):
        '''
        Set delivery fee is 0,if the cart_value is greater than or equal to 200€(20000 cents)
        '''
        if self.cart_value >=20000:
            self.delivery_fee=0

    def delivery_Fee_Friday_Rush(self):
        '''
        Check if the delivery time is within the Friday rush period (3 - 7 PM UTC)
        '''
        if self.delivery_time.weekday() == 4:
            start_time = datetime(self.delivery_time.year,self.delivery_time.month,self.delivery_time.day, 15, 0, 0, tzinfo=pytz.utc)
            end_time = datetime(self.delivery_time.year,self.delivery_time.month,self.delivery_time.day, 19, 0, 0, tzinfo=pytz.utc)
            if start_time <= self.delivery_time <= end_time:
                self.delivery_fee *= 120
            self.delivery_Fee_Limit()

    def post(self):
        self.cart_Value_Surcharge()
        self.distance_Delivery()
        self.no_Of_Items_Delivery()
        self.delivery_Fee_Limit()
        self.delivery_Fee_Free()
        self.delivery_Fee_Friday_Rush()
        return jsonify({"delivery_fee": self.delivery_fee})
