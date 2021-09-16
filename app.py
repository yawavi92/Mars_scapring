#Dependencies
from flask import Flask, render_template, redirect, url_for
import scrape_mars
import pymongo
import pandas as pd


app = Flask(__name__)

#use flask_pymongo to set up mongo conncetion 
conn = "mongodb://localhost:27017/mars_app"
client = pymongo.MongoClient(conn)
#mars_db = client.db.mars

#root taht queries Mongo DB and pass in mars as html 
@app.route("/")
def index():
    mars_data = client.db.mars.find_one()
    return render_template("index.html", mars = mars_data)

#
@app.route("/scrape")
def scrape():
    #Run the scrape function
    mars = scrape_mars.scrape_all()
    #Update the Mongo database using update and upsert=True
    client.db.mars.update({}, mars, upsert = True)
    return redirect("/")

if __name__ == "__main__":
   app.run(debug=True)