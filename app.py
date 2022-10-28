# https://icalendar.readthedocs.io/en/latest/api.html
from datetime import date
from icalendar import Calendar, Event
import requests
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)

cal_feed_url = "http://stevenscoop.myschoolapp.com/podium/feed/iCal.aspx?z=EDb8RhfnZRh4jlgx9PDUaR03lkjDvMG7nV%2brhHrb7XbZgJsRtvBfjkV2it8mhyxcYCfWYJ5XB7xTMcJ2vTUr0Q%3d%3d"
today = date.today()

@app.route("/")
def what_day_is_it():
    
    # fetch the cal feed
    headers = {
        'User-Agent': 'M',
        }
    response = requests.get(cal_feed_url, headers=headers)
    
    # parse it
    stevens_cal = Calendar.from_ical(response.text)

    #TODO: find today's date, any events with "Day " and then parse the integer from [-1]
    
    day = '?'
    
    for component in stevens_cal.walk():
        if component.name == "VEVENT":
            if component.decoded("dtstart") == today:
                if component.get("summary")[0:7] == "LAB Day":
                    day = "LAB Day"
                elif component.get("summary")[0:4] == "Day ":
                    day = f'Day {component.get("summary")[-1]}'
                else:
                    day = "School is not in session"

    return render_template('index.html', today=today.strftime('%B %-d, %Y'), day=day)

