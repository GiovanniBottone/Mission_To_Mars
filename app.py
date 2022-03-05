from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# For above code:
# The first line says that we'll use Flask to render a template, redirecting to another url, and creating a URL.
# The second line says we'll use PyMongo to interact with our Mongo database.
# The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.

# Under these lines, let's add the following to set up Flask:
app = Flask(__name__)

# We also need to tell Python how to connect to Mongo using PyMongo.
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# For the above code:
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".

# Set Up App Routes
# define the route for the HTML page.
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# This route, @app.route("/"), tells Flask what to display when we're looking at the home page
# Within the def index(): function the following is accomplished:
# mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database, which we will create when we convert our Jupyter scraping code to Python Script.
# We will also assign that path to themars variable for use later.
# return render_template("index.html" tells Flask to return an HTML template using an index.html file.
# mars=mars) tells Python to use the "mars" collection in MongoDB.

@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# The first line, @app.route(“/scrape”) defines the route that Flask will be using.
# The next lines allow us to access the database, scrape new data using our scraping.py script, update the database, and return a message when successful.
# First, we define it with def scrape():.
# Then, we assign a new variable that points to our Mongo database: mars = mongo.db.mars.
# Next, we created a new variable to hold the newly scraped data: mars_data = scraping.scrape_all().
# Next, we'll use the data we have stored in mars_data. The syntax used here is {"$set": data}. This means that the document will be modified ("$set") with the data in question.
# Finally, the option we'll include is upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved (even if we haven't already created a document for it).

if __name__ == "__main__":
   app.run()