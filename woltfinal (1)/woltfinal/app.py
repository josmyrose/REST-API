from flask import Flask, request
from flask_restful import Api, Resource
from Delivery_fee_Calculator import Delivery_fee_Calculator

app = Flask(__name__)
api = Api(app)

api.add_resource(Delivery_fee_Calculator, '/Delivery')

if __name__ == '__main__':
    #app.run(debug=True)
    try:
        app.run()
    except:
        print('Unable to open port')