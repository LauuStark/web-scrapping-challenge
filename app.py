from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

mongo = client.mars_db


@app.route("/")
def index():
    mars = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars)

@app.route('/scrape')
def scrape():
    mars = mongo.db.mars
    marsdata = scrape_mars.scrape()
    mongo.db.collection.update({}, marsdata, upsert=True)
    return redirect("/")



if __name__ == "__main__":
    app.run()