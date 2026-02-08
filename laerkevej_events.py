from ics import Calendar, Event
from datetime import datetime, timedelta, timezone
import os
from ics.grammar.parse import ContentLine

try:
    import zoneinfo # Python 3.9+
except ImportError:
    from backports import zoneinfo # For older Python versions

# Path to the file you want to delete
file_path = "laerkevej_events.ics"

# Check if the file exists before attempting to delete it
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File '{file_path}' has been deleted successfully.")
else:
    print(f"File '{file_path}' does not exist.")

birthdays = [
  {
    "date": "2024-01-02",
    "name": "Carl-Emil",
    "number": 3
  },
  {
    "date": "2026-01-18",
    "name": "Silke",
    "number": 1
  },
  {
    "date": "2024-02-09",
    "name": "Astrid",
    "number": 10
  },
  {
    "date": "2024-02-13",
    "name": "Cecilie",
    "number": 1
  },
  {
    "date": "2024-02-23",
    "name": "Stine",
    "number": 10
  },
  {
    "date": "2024-03-10",
    "name": "Lara",
    "number": 4
  },
  {
    "date": "2024-03-17",
    "name": "Louise",
    "number": 4
  },
  {
    "date": "2024-03-21",
    "name": "Carl",
    "number": 9
  },
  {
    "date": "2024-03-28",
    "name": "Karin",
    "number": 7
  },
  {
    "date": "2024-03-29",
    "name": "Sigrid",
    "number": 10
  },
  {
    "date": "2024-04-14",
    "name": "Jakob",
    "number": 2
  },
  {
    "date": "2024-04-15",
    "name": "Jonas",
    "number": 2
  },
  {
    "date": "2024-04-16",
    "name": "Finn",
    "number": 11
  },
  {
    "date": "2024-04-21",
    "name": "Christian",
    "number": 4
  },
  {
    "date": "2024-04-22",
    "name": "Lissen",
    "number": 5
  },
  {
    "date": "2024-05-06",
    "name": "Eleonora",
    "number": 16
  },
  {
    "date": "2024-05-08",
    "name": "Louise",
    "number": 3
  },
  {
    "date": "2024-05-18",
    "name": "Christian",
    "number": 1
  },
  {
    "date": "2024-05-21",
    "name": "Amalie",
    "number": 6
  },
  {
    "date": "2024-05-26",
    "name": "Helene",
    "number": 6
  },
  {
    "date": "2024-06-01",
    "name": "Carl Erik",
    "number": 5
  },
  {
    "date": "2024-06-05",
    "name": "Martha",
    "number": 9
  },
  {
    "date": "2024-06-14",
    "name": "Liva",
    "number": 16
  },
  {
    "date": "2024-07-02",
    "name": "Christina",
    "number": 8
  },
  {
    "date": "2024-07-24",
    "name": "Jack",
    "number": 6
  },
  {
    "date": "2024-08-08",
    "name": "Christian",
    "number": 10
  },
  {
    "date": "2024-08-12",
    "name": "Alice",
    "number": 12
  },
  {
    "date": "2024-08-12",
    "name": "Mads",
    "number": 8
  },
  {
    "date": "2024-08-17",
    "name": "Henrik",
    "number": 2
  },
  {
    "date": "2024-09-09",
    "name": "Mathias",
    "number": 8
  },
  {
    "date": "2024-09-09",
    "name": "Oscar",
    "number": 3
  },
  {
    "date": "2024-09-11",
    "name": "Nicoline",
    "number": 8
  },
  {
    "date": "2024-09-20",
    "name": "Høgni",
    "number": 16
  },
  {
    "date": "2024-09-30",
    "name": "Inge",
    "number": 11
  },
  {
    "date": "2024-10-01",
    "name": "Marie",
    "number": 4
  },
  {
    "date": "2024-10-02",
    "name": "Tom",
    "number": 14
  },
  {
    "date": "2024-10-15",
    "name": "Pernille",
    "number": 14
  },
  {
    "date": "2024-11-01",
    "name": "Hans Henrik",
    "number": 3
  },
  {
    "date": "2024-11-27",
    "name": "Anika",
    "number": 16
  },
  {
    "date": "2024-12-16",
    "name": "Rasmus",
    "number": 4
  },
  {
    "date": "2024-12-18",
    "name": "Louise",
    "number": 2
  },
  {
    "date": "2024-12-30",
    "name": "Aage",
    "number": 7
  }
]

events = [
    # {
    #     "name": "Vejfest7", 
    #     "description": "Husk drikkevarer", 
    #     "start": "2026-02-11 12:00", 
    #     "end": "2026-02-11 23:59"
    # }
]

cal = Calendar()
cal.extra.append(ContentLine(name="METHOD", value="PUBLISH"))
cal.extra.append(ContentLine(name="X-WR-CALNAME", value="Lærkevej begivenheder"))
cal.extra.append(ContentLine(name="REFRESH-INTERVAL", value="PT12H"))
cal.extra.append(ContentLine(name="X-APPLE-DEFAULT-ALARM", value="TRUE"))

def add_apple_alarm(event, hours_before, summary="Påmindelse"):
    """Using a more explicit trigger format for iOS subscriptions."""
    event.extra.append(ContentLine(name="BEGIN", value="VALARM"))
    event.extra.append(ContentLine(name="ACTION", value="DISPLAY"))
    event.extra.append(ContentLine(name="DESCRIPTION", value=summary))
    # This format is often more successful in subscriptions:
    # RELATED=START explicitly tells the server when to count from
    event.extra.append(ContentLine(name="TRIGGER;RELATED=START", value=f"-PT{hours_before}H"))
    event.extra.append(ContentLine(name="END", value="VALARM"))

now = datetime.now()

for bday in birthdays:
    event_date = datetime.fromisoformat(bday["date"])
    e = Event()
    event_name = f"🇩🇰 - {bday['name']} i nr. {bday['number']} har fødselsdag"
    e.name = event_name
    e.begin = event_date
    e.make_all_day()
    e.description = f"Husk at sætte flag ud for {bday['name']} 🇩🇰"
    e.created = now
    e.extra.append(ContentLine(name="RRULE", value="FREQ=YEARLY"))
    add_apple_alarm(e, 7, summary=f"Fødselsdag i morgen: {bday['name']}")
    cal.events.add(e)

for event in events:
    e = Event()
    e.name = event["name"]
    e.description = event.get("description", "")
    # Start and end time
    dk_tz = zoneinfo.ZoneInfo("Europe/Copenhagen")
    # Parse the time from your list
    naive_dt = datetime.strptime(event["start"], "%Y-%m-%d %H:%M")
    naive_end = datetime.strptime(event["end"], "%Y-%m-%d %H:%M")
    # This automatically detects if it's +1 (Winter) or +2 (Summer)
    local_start = naive_dt.replace(tzinfo=dk_tz)
    local_end = naive_end.replace(tzinfo=dk_tz)
    # Convert to UTC for the .ics file
    e.begin = local_start.astimezone(timezone.utc)
    e.end = local_end.astimezone(timezone.utc)
    e.created = now 
    add_apple_alarm(e, 1, summary=f"Husk: {event['name']}")
    cal.events.add(e)

# Clean Save (Binary mode to prevent blank lines)
raw_content = cal.serialize()
lines = [line.strip() for line in raw_content.splitlines() if line.strip()]
clean_content = "\r\n".join(lines) + "\r\n"

with open(file_path, "wb") as f:
    f.write(clean_content.encode('utf-8'))

print("ics file sucessfully generated!")
# Validator: https://icalendar.org/validator.html