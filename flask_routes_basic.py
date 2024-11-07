from flask import Flask
app = Flask(__name__)

# Creating the flask route, you can make multiple routes. always put the function on the next line as the route will run the function
@app.route("/") # after the slash anything can be written as a pagename
def home():
    return "Welcome to the Flask Music Festival"

# if __name__ == "__main__": # This will run the flask program but this is not the proper way to run it
#     app.run(debug=True)

# The proper way to run a flask application is "flask run" in the terminal