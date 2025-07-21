from flask import Flask, jsonify, render_template
from flask_cors import CORS
from auth import check_token_expiration
from manage_tokens import *
import requests
import os

cost_of_journey = 3.8

info = read_from_file()
ACCESS_TOKEN = info['access_token']

def get_activities():
  check_token_expiration(info)
  activities = []
  page_size = 200
  page = 1
  after = "1745848191"
  
  while True:
    url = f"https://www.strava.com/api/v3/activities?access_token={ACCESS_TOKEN}&after={after}&per_page={page_size}&page={page}"
    payload = {}
    
    response = requests.request("GET", url, data=payload)
    
    if response.status_code != 200:
      raise Exception(f"Failed to fetch activities: {response.status_code} - {response.text}")
    
    data = response.json()
    print(f"len data (page:{page}):" + str(len(data)))
    
    for i in data:
      activities.append(i)
      
    if len(data) < page_size:
        break  # Last page reached
    
    page += 1
  print(f"first: {len(activities)}")
  return activities

def journey_count():
  commutes = []
  for i in get_activities():
    if i['commute'] == True:
      commutes.append(i)
  journeys = int(len(commutes))
  return journeys

def calc_savings(cost_of_journey):
  count = journey_count()
  saved = count * cost_of_journey
  return {
    "total_saved": saved, "journey_count": count
  }

app = Flask(__name__)

frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5500")
CORS(app, origins=[frontend_origin])

@app.route("/api/savings")
def savings():
  savings = calc_savings(cost_of_journey)
  return jsonify(savings)

@app.route("/")
def index():
  return render_template('index.html')

if __name__ == '__main__': 
  app.run(debug = True)

if __name__ == '__main__':
    env = os.getenv("FLASK_ENV", "development")
    debug = env == "development"

    app.run(
        debug=debug,
        host='0.0.0.0' if env == "production" else '127.0.0.1',
        port=int(os.getenv("PORT", 5000))
    )