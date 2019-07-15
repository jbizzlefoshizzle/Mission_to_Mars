from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# Always begin with:
app = Flask(__name__)

# First route
@app.route("/")
def index(): # Where to do render template


@app.route("/scrape") # Where to do scrape
def scrape():
    mars_data = scrape_mars.scrape_all() # Call scrape_all from scrape_mars.py

# Always end with:
if __name__ == "main":
    app.run()