# Import as needed
import mysql.connector # for database connection
from mysql.connector import Error # for database errors
from flask import Flask, jsonify, request # for flask, marshmallow, request, and serializing/deserializing JSON
from flask_marshmallow import Marshmallow # for data validation
from marshmallow import fields, ValidationError # for use of fields and validation error
from my_password import my_password 

app = Flask(__name__) # Initializing flask
ma = Marshmallow(app) # Initializing marshmallow

# Defining the schema for data validation
class CustomerSchema(ma.Schema):
    name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta: # Options object for schema
        fields = ("name", "email", "phone", "id") # Required list of fields to be included with serialization

customer_schema = CustomerSchema() # Managing one 'customer'
customers_schema = CustomerSchema(many=True) # Managing all 'customers'

# Function to open a database connection
def get_db_connection():
    # Database Connection Parameters:
    db_name = "e_commerce_db"
    user = "root"
    password = my_password
    host = "localhost"


    try: # Establishing the database connection
        conn = mysql.connector.connect(
	        database=db_name,
	        user=user,
	        password=password,
	        host=host
        )

        return conn

    except Error as e: # Error handling
        print(f"Error: {e}")

# Creating the flask route for home
@app.route("/") # after the slash anything can be written as a pagename
def home():
    return "Welcome to the Flask Music Festival"

# Creating flask route for get customers
@app.route('/customers', methods=['GET'])
def get_customers():
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verify vonnecction
            return jsonify({"error:": "Database connecction failed"}), 500 # Converting error message
        cursor = conn.cursor(dictionary=True) # Activate cursor
        query = "SELECT * FROM Customers" # Define query
        cursor.execute(query) # Execute query
        customers = cursor.fetchall() # Insert data into variable
        return customers_schema.jsonify(customers) # Convert data according to schema
    except Error as e:
        print(f"Error: {e}") # Display message to user
        return jsonify({"error": "Internal Server Error"}), 500 # Converting error message
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Creating flask route to add a new customer
@app.route('/customers', methods=['POST'])
def add_customer():
    try:
        customer_data = customer_schema.load(request.json) # Verifying data
    except ValidationError as e:
        print(f"Error: {e}") # Display message to user
        return jsonify(e.messages), 400 # Converting error message, 400 indicates error type
    
    try:
        conn = get_db_connection() # Establishing database connection
        if conn is None: # Verifying connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Display message to user
        cursor = conn.cursor() # Activate cursor
        
        new_customer = (customer_data['name'], customer_data['email'], customer_data['phone']) # Inserting data into variable for query
        
        query = "INSERT INTO Customers (name, email, phone) VALUES (%s, %s, %s)" # Defining query to add new customer
        
        cursor.execute(query, new_customer) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "New customer added successfully"}), 201 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Creating flask route to update a customer
@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    try:
        customer_data = customer_schema.load(request.json) # Verifying data
    except ValidationError as e:
        print(f"Error: {e}") # Display error message to user
        return jsonify(e.messages), 400 # Converting error message, 400 indicates error type
    
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Displaying error message if database connection unsuccessful
        cursor = conn.cursor() # Activate cursor
        
        updated_customer = (customer_data['name'], customer_data['email'], customer_data['phone'], id) # Inserting update data into a variable for query

        query = "UPDATE Customers SET name = %s, email = %s, phone = %s WHERE id = %s" # Defining query

        cursor.execute(query, updated_customer) # Execute query
        conn.commit() # Commit changes to database

        return jsonify({"message": "Customer updated successfully"}), 201 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()

# Creating flask route to delete a customer
@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    try:
        conn = get_db_connection() # Establish database connection
        if conn is None: # Verifying database connection
            return jsonify({"error:": "Database connecction failed"}), 500 # Displaying error message if database connection unsuccessful
        cursor = conn.cursor() # Activate cursor
        
        customer_to_remove = (id,) # Inserting data into variable for query

        cursor.execute("SELECT * FROM Customers WHERE id = %s", customer_to_remove) # Execute query to get customer
        customer = cursor.fetchall()
        if not customer: # Verifying customer exists
            return jsonify({"error": "Customer not found"}), 404 # Display message to user

        query = "DELETE FROM Customers WHERE id = %s" # Defining query to delete customer
        cursor.execute(query, customer_to_remove) # Execute query
        conn.commit() # Commit changes to database
        
        return jsonify({"message": "Customer removed successfully"}), 200 # Display message to user
    except Error as e:
        print(f"Error: {e}") # Display message to user

        return jsonify({"error": "Internal Server Error"}), 500 # Display message to user
    finally:
        if conn and conn.is_connected(): # Close connection
            cursor.close()
            conn.close()
    
if __name__ == "__main__": # This will run the flask program but this is not the proper way to run it
    app.run(debug=True)