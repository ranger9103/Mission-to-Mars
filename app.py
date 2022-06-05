from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")


@app.route("/")
def home():
   mars_data = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():
   scraper = scraping.scrape_all()
   mars_data = scraper.scrape_info()
   mars_info = mongo.db.mars_info
   mars_info.update_one({}, {"$set": mars_data}, upsert=True)

   return redirect('/')
   
if __name__ == "__main__":
   app.run(debug=True)

