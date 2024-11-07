# Import as needed
import mysql.connector
from mysql.connector import Error
from flask import Flask
from flask_marshmallow import Marshmallow
from marshmallow import fields
from my_password import my_password

app = Flask(__name__)
ma = Marshmallow(app)

# Defining the schema for data validation
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta: # Options object for schema
        fields = ("name", "email", "phone") # Required list of fields to be included with serialization

customer_schema = CustomerSchema() # Managing one 'customer'
customers_schema = CustomerSchema(many=True) # Managing all 'customers'

# Creating the flask route, you can make multiple routes. always put the function on the next line as the route will run the function
@app.route("/") # after the slash anything can be written as a pagename
def home():
    return "Welcome to the Flask Music Festival"

if __name__ == "__main__": # This will run the flask program but this is not the proper way to run it
    app.run(debug=True)