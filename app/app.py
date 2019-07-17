from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Always begin with:
app = Flask(__name__)

client = PyMongo.MongoClient()
db = client.mars_db
collection = db.mars_data

# First route
@app.route("/")
def index(): # Where to do render template
    mars_data = list(db.collection.find())[0]

    return render_template('index.html', mars_data = mars_data)


@app.route("/scrape") # Where to do scrape
def scrape():
    # Remove collection if need be
    db.collection.remove({})
    mars_data = scrape_mars.scrape_all() # Call scrape_all from scrape_mars.py
    db.collection.insert_one(mars_data)

    return render_template('scrape.html')

# Always end with:
if __name__ == "main":
    app.run()