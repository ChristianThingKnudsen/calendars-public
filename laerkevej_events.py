from ics import Calendar, Event
from datetime import datetime, timedelta
import os
from ics.grammar.parse import ContentLine

# Path to the file you want to delete
file_path = "laerkevej_events.ics"

# Check if the file exists before attempting to delete it
if os.path.exists(file_path):
    os.remove(file_path)
    print(f"File '{file_path}' has been deleted successfully.")
else:
    print(f"File '{file_path}' does not exist.")

# Data structured as per the user's request
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
    {
        "name": "Vejfest", 
        "description": "Husk drikkevarer", 
        "start": "2026-02-09 16:00", 
        "end": "2026-02-09 23:59"
    },
    # {
    #     "name": "Vejfes2", 
    #     "description": "Husk drikkevarer", 
    #     "start": "2026-02-10 16:00", 
    #     "end": "2026-02-10 23:59"
    # }
]

def add_alarm(event, hours_before):
    """Adds a custom VALARM block to the event's extra lines."""
    alarm_block = (
        f"BEGIN:VALARM\n"
        f"TRIGGER:-PT{hours_before}H\n"
        f"ACTION:DISPLAY\n"
        f"DESCRIPTION:Reminder\n"
        f"END:VALARM"
    )
    event.extra.append(ContentLine(name="VALARM_BLOCK", value=alarm_block))

# Create a new calendar
cal = Calendar()

print(f"Creating ics file with events {len(birthdays)} events...")
# Add events to the calendar
for bday in birthdays:
    event_date = datetime.fromisoformat(bday["date"])
    event = Event()
    event.name = bday["name"]
    print(f"Adding: {event.name}...")
    event.begin = event_date
    event.name = f"🇩🇰 - {bday['name']} i nummer {bday['number']} har fødselsdag"
    event.description = f"Husk at sætte flag ud for {bday['name']}"
    event.make_all_day()

    # Set the event to recur yearly
    event.extra.append(ContentLine(
            name="RRULE", value=f"FREQ=YEARLY;"))
    
    # Add the event to the calendar
    add_alarm(event, 7) # 7 hours before
    cal.events.add(event)

for event in events:
    e = Event()
    e.name = event["name"]
    e.description = event.get("description","")
    e.begin = datetime.strptime(event["start"], "%Y-%m-%d %H:%M")
    e.end = datetime.strptime(event["end"], "%Y-%m-%d %H:%M")
    add_alarm(e, 1) # 1 hour before
    cal.events.add(e)

# Serialize the calendar to a string
ics_content = str(cal)

# Insert VALARM block for each event with 7-hour prior trigger
ics_content = ics_content.replace(
    "END:VEVENT",
    "BEGIN:VALARM\nTRIGGER:-PT7H\nACTION:DISPLAY\nDESCRIPTION:Reminder\nEND:VALARM\nEND:VEVENT"
)

# Save the updated ICS content to a file
with open(file_path, "w") as f:
    f.write(ics_content)

print("Succesfully created ics file!")
# print("ICS file with exact 17:00 day-before alarms created successfully!")