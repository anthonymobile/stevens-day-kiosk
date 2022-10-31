# https://icalendar.readthedocs.io/en/latest/api.html
from datetime import date, datetime, timedelta
from icalendar import Calendar, Event
import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
# app = Flask(__name__,
#             static_folder="public", 
#             static_url_path="/static")
bootstrap = Bootstrap5(app)

cal_feed_url = "http://stevenscoop.myschoolapp.com/podium/feed/iCal.aspx?z=EDb8RhfnZRh4jlgx9PDUaR03lkjDvMG7nV%2brhHrb7XbZgJsRtvBfjkV2it8mhyxcYCfWYJ5XB7xTMcJ2vTUr0Q%3d%3d"
today = date.today()
tomorrow = date.today() + timedelta(days=1)
now = datetime.now()

@app.route("/")
def what_day_is_it():
    
    # fetch the cal feed
    headers = {
        'User-Agent': 'M',
        }
    response = requests.get(cal_feed_url, headers=headers)
    
    # parse it
    stevens_cal = Calendar.from_ical(response.text)

    #TODO: update to also pass motw
    motd = 'not a school day'
    motw = 'not a school day'
    
    for component in stevens_cal.walk():
        if component.name == "VEVENT":
            
            # find today 
            if component.decoded("dtstart") == today:
                if component.get("summary")[0:7] == "LAB Day":
                    motd = "LAB Day"
                elif component.get("summary")[0:4] == "Day ":
                    motd = f'Day {component.get("summary")[-1]}'
                    
            # fidn tomorrow
            if component.decoded("dtstart") == tomorrow:
                if component.get("summary")[0:7] == "LAB Day":
                    motw = "LAB Day"
                elif component.get("summary")[0:4] == "Day ":
                    motw = f'Day {component.get("summary")[-1]}'

    return render_template('index.html',
                           now=now, 
                           dow=today.strftime('%A'), 
                           today=today.strftime('%A %B %-d, %Y'),
                           motd=motd,
                           tdow=tomorrow.strftime('%A'),
                           tomorrow=tomorrow.strftime('%A %B %-d, %Y'),
                           motw=motw
                           )

