import requests
import json
import mysql.connector
import subprocess 
from textblob import TextBlob  


url = "https://rss.app/feeds/v1.1/GSRNQ3wg7plHCI3Q.json"

def analyze_sentiment(description):
  
    analysis = TextBlob(description)
    

    if analysis.sentiment.polarity > 0:
        return "positive"
    elif analysis.sentiment.polarity < 0:
        return "negative"
    else:
        return "neutral"


db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="ivica15%",
    database="twitterapp"
)
cursor = db.cursor()


response = requests.get(url)


if response.status_code == 200:
 
    data = response.json()


    items = data.get("items", [])
    for item in items:
        item_id = item.get("id")
        item_description = item.get("title")
        item_date = item.get('date_published');
        
        colon_index = item_description.find(':')
        item_description = item_description[colon_index + 2:]
        

        
        cursor.execute("SELECT id FROM analysis WHERE id = %s", (item_id,))
        existing_item = cursor.fetchone()

        if not existing_item:
            
            sentiment_result = analyze_sentiment(item_description)

            if sentiment_result != "neutral":
                
                cursor.execute("INSERT INTO analysis (ID, Text,Date,Result) VALUES (%s, %s, %s, %s)",
                               (item_id, item_description, item_date, sentiment_result))
                db.commit()

  
    db.close()



else:
    print(f"Failed to retrieve data from the API. Status Code: {response.status_code}")


script_path = "generatePDF.py"
subprocess.run(["python", script_path], check=True)
  
