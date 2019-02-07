from flask import Flask,render_template,request
import tweepy
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os 

#My Twitter API Authentication Variables
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')

app = Flask(__name__)
# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

sid = SentimentIntensityAnalyzer()


def color(x):

    if x > 0.05:
        return "bg-success"
    elif x > -0.05 and x < 0.05:
        return "bg-white"
    else:
        return "bg-danger"


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        
        tweets = api.search(request.form.get("input"), count=500)
        data=[tweet.text for tweet in tweets]

        sentiment =[sid.polarity_scores(tweet)['compound'] for tweet in data]
        
        df=pd.DataFrame({'tweet': data,'senti': sentiment})
        df['senti']=df['senti'].apply(color)
        
        page_data=df.to_dict('records')
        
        return render_template("index.html",data=page_data)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)