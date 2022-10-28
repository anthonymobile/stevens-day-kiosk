# https://icalendar.readthedocs.io/en/latest/api.html
from datetime import date
from icalendar import Calendar, Event
import requests
from flask import Flask
app = Flask(__name__)

cal_feed_url = "http://stevenscoop.myschoolapp.com/podium/feed/iCal.aspx?z=EDb8RhfnZRh4jlgx9PDUaR03lkjDvMG7nV%2brhHrb7XbZgJsRtvBfjkV2it8mhyxcYCfWYJ5XB7xTMcJ2vTUr0Q%3d%3d"
today = date.today()

def render_page(today, day):
    html = f"<h1>Today is {today}. It is Day {day} at Stevens.</h1> <P>This app fetches the Stevens school day calendar and display the current day number.</P>"
    return html

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
    
    for component in stevens_cal.walk():
        if component.name == "VEVENT":
            if component.decoded("dtstart") == today:
                if component.get("summary")[0:4] == "Day ":
                    print(component.decoded("dtstart"))
                    print(component.get("summary"))
                    day = component.get("summary")[-1]
    return render_page(today, day)
