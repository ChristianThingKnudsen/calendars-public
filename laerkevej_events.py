from ics import Calendar, Event
from datetime import datetime, timedelta, timezone
import requests
import json
import os
from ics.grammar.parse import ContentLine
from data import birthdays, events
from email_utils import send_error_email
import urllib.request
import traceback
try:
    import zoneinfo # Python 3.9+
except ImportError:
    from backports import zoneinfo # For older Python versions

try:

  def print_separator(char='=', length=50):
      """
      Prints a separator line to the console.

      Parameters:
      char (str): The character to use for the separator. Default is '-'.
      length (int): The length of the separator line. Default is 50.
      """
      print(char * length)

  print_separator()
  # Get the current time
  current_time = datetime.now()
  # Format the time in a readable format
  formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

  # Print the formatted time
  print(formatted_time)
  print_separator()

  # Path to the file you want to delete
  file_path = "laerkevej_events.ics"

  # Check if the file exists before attempting to delete it
  if os.path.exists(file_path):
      os.remove(file_path)
      print(f"File '{file_path}' has been deleted successfully.")
  else:
      print(f"File '{file_path}' does not exist.")

  def trash_prefix(last):
      return "🗑️ - " + last

  def trash_event_to_name(event):
      fractions = event["fraktioner"]

      if not fractions:
          return ""
      elif len(fractions) == 1:
          return trash_prefix(fractions[0])
      # Join all elements except the last one with ", "
      result = ", ".join(fractions[:-1])
      # Add " og " before the last element
      result += " og " + fractions[-1]
      return trash_prefix(result)

  def get_trash_event_date(event):
      # Parse the date string into a datetime object
      date_str = event["dato"]
      event_datetime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
      # Subtract one day
      event_datetime = event_datetime - timedelta(days=1)
      # Set the time to 08:00 AM
      event_datetime = event_datetime.replace(hour=20, minute=0, second=0, microsecond=0)
      # Return the modified datetime
      return event_datetime


  def add_apple_alarm(event, hours_before, summary="Påmindelse"):
      """Using a more explicit trigger format for iOS subscriptions."""
      event.extra.append(ContentLine(name="BEGIN", value="VALARM"))
      event.extra.append(ContentLine(name="ACTION", value="DISPLAY"))
      event.extra.append(ContentLine(name="DESCRIPTION", value=summary))
      # This format is often more successful in subscriptions:
      # RELATED=START explicitly tells the server when to count from
      event.extra.append(ContentLine(name="TRIGGER;RELATED=START", value=f"-PT{hours_before}H"))
      event.extra.append(ContentLine(name="END", value="VALARM"))

  cal = Calendar()
  cal.extra.append(ContentLine(name="METHOD", value="PUBLISH"))
  cal.extra.append(ContentLine(name="X-WR-CALNAME", value="Lærkevej begivenheder"))
  cal.extra.append(ContentLine(name="REFRESH-INTERVAL", value="PT12H"))
  cal.extra.append(ContentLine(name="X-APPLE-DEFAULT-ALARM", value="TRUE"))

  now = datetime.now()

  for bday in birthdays:
      event_date = datetime.fromisoformat(bday["date"])
      e = Event()
      show_age = bday.get("showBirthYear", False)
      event_name = f"🇩🇰 - {bday['name']} i nr. {bday['number']} "
      if show_age:
          age = now.year - event_date.year
          # Round birthday
          if age > 0 and age % 10 == 0:
              event_name += f"fylder rund ({age}) 🍾"
          else:
              event_name += f"har fødselsdag"
      else:
          event_name += f"har fødselsdag"
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


  # Old trash events (for history)
  trash_history_file = "trash_history.json"
  trash_history_data = []
  if os.path.exists(trash_history_file):
      with open(trash_history_file, 'r', encoding='utf-8') as f:
          try:
              trash_history_data = json.load(f)
          except json.JSONDecodeError:
              trash_history_data = []

  print(trash_prefix(f"Fandt {len(trash_history_data)} tidligere tømninger der tilføjes nu"))

  # Extract dates we already have to avoid duplicates
  existing_trash_dates = {item["dato"] for item in trash_history_data}

  # Dynamic trash events
  url = "https://mit.renosyd.dk/_query/tommekalender-page-content.Hent%20T%C3%B8mmekalender"
  body = {
      "url": "https://skoda-selvbetjeningsapi.renosyd.dk/api/v1/toemmekalender?nummer=018615",
      "method": "GET",
      "auth": None,
      "headers": {}
  }
  trash_data = {}
  cache_file = "trash_data_fallback.json"
  response = requests.post(url, json=body, timeout=15)
  try:
      response = requests.post(url, json=body, timeout=15)
      if response.status_code == 200:
          json_data = response.json()
          # Double-check we actually got data before saving
          if json_data and len(json_data) > 0:
              trash_data = json_data[0]
              # Save the "Last Known Good" version
              with open(cache_file, 'w') as f:
                  json.dump(trash_data, f, indent=4)
              print(trash_prefix("Sucessfully retrieved trash data from api!"))
          else:
              print(trash_prefix("API returned empty list. Falling back..."))
              raise ValueError("Empty Data")

      else:
          print(trash_prefix(f"API Error {response.status_code}. Falling back..."))
          raise ConnectionError

  except (requests.exceptions.RequestException, ValueError, ConnectionError, IndexError):
      # Try to load the file saved from a previous successful run
      if os.path.exists(cache_file):
          with open(cache_file, 'r') as f:
              trash_data = json.load(f)
              print(trash_prefix(f"Using fallback data from {cache_file}"))
      else:
          print(trash_prefix("No fallback file found and API failed."))
          trash_data = {} # Final fallback to empty object

  upcoming_empties = trash_data.get("planlagtetømninger", [])
  if not isinstance(upcoming_empties, list):
      upcoming_empties = []

  # Fake test event
  # fake_event = {
  #     "dato": "2026-02-10T00:00:00Z",  # Use a date in the near future
  #     "fraktioner": ["Restaffald", "Genbrug"]
  # }
  # upcoming_empties.append(fake_event)

  new_history_added = False
  current_date_iso = datetime.now(timezone.utc).date().isoformat()
  # Fake current date if nessecary for test
  # current_date_iso = (datetime.now(timezone.utc) + timedelta(days=8)).date().isoformat()

  for entry in upcoming_empties:
      if entry["dato"] not in existing_trash_dates:
          event_date = entry["dato"].split("T")[0]
          if event_date <= current_date_iso:
              trash_history_data.append(entry)
              existing_trash_dates.add(entry["dato"])
              new_history_added = True
              print(trash_prefix(f"Archived past event: {entry['dato']}"))

  if new_history_added:
      print("Trash event(s) added to history")
      trash_history_data.sort(key=lambda x: x["dato"])
      with open(trash_history_file, 'w', encoding='utf-8') as f:
          json.dump(trash_history_data, f, indent=4, ensure_ascii=False)
  else:
      print("No trash events added to history")


  number_of_trash_events = len(upcoming_empties)
  raw_future_events = upcoming_empties[:9] if number_of_trash_events >= 9 else upcoming_empties
  # Ensure no duplicate events are made
  future_trash_events = [
      e for e in raw_future_events
      if e["dato"] not in existing_trash_dates
  ]
  trash_events_to_process = future_trash_events + trash_history_data

  print(trash_prefix(f"Fandt {len(trash_events_to_process)} tømninger der tilføjes nu"))

  for trash_event in trash_events_to_process:
    e = Event()
    event_name = trash_event_to_name(trash_event)
    e.name = event_name
    e.description = trash_prefix("Skrald hentes i morgen tidlig, så det skal stilles ud til vejen nu")
    # Start and end time
    dk_tz = zoneinfo.ZoneInfo("Europe/Copenhagen")
    # Parse the time from your list
    naive_dt = get_trash_event_date(trash_event)
    naive_end = naive_dt + timedelta(hours=2)
    # This automatically detects if it's +1 (Winter) or +2 (Summer)
    local_start = naive_dt.replace(tzinfo=dk_tz)
    local_end = naive_end.replace(tzinfo=dk_tz)
    # Convert to UTC for the .ics file
    e.begin = local_start.astimezone(timezone.utc)
    e.end = local_end.astimezone(timezone.utc)
    e.created = now
    add_apple_alarm(e, 3, summary=f"Husk: {event_name}")
    cal.events.add(e)


  #Electric events
  electric_incidents_url = "https://api.elnet.greenpowerdenmark.dk/api/incidents?showType=1&skip=0&supplierId=14&top="

  with urllib.request.urlopen(electric_incidents_url) as response:
    incidents = json.loads(response.read())

  skanderborg_incidents = [
    i for i in incidents
    if "8660" in (i.get("zipcodes") or "").split(",")
    or "Skanderborg" in (i.get("title") or "")
    or "Skanderborg" in (i.get("cause") or "")
  ]

  if skanderborg_incidents:
    for i in skanderborg_incidents:
        print(f"{i['title']} ({i['incidentType']})")
        print(f"  Start: {i['startDate']}")
        print(f"  Forventet afslutning: {i['expectedDowntime']}")
        print(f"  Berørte kunder: {i['effectedCustomers']}")
        print(f"  Årsag: {i['cause']}")

        # Add calendar event
        e = Event()
        e.name = f"🔌 - {i['title']}"
        e.description = i.get("cause", "")
        dk_tz = zoneinfo.ZoneInfo("Europe/Copenhagen")
        start_dt = datetime.fromisoformat(i["startDate"]).replace(tzinfo=dk_tz)
        end_dt = datetime.fromisoformat(i["expectedDowntime"]).replace(tzinfo=dk_tz)
        e.begin = start_dt.astimezone(timezone.utc)
        e.end = end_dt.astimezone(timezone.utc)
        e.created = now
        add_apple_alarm(e, 1, summary=f"Strømafbrud: {i['title']}")
        cal.events.add(e)
  else:
    print("Ingen aktive hændelser i Skanderborg (8660)")

  # Clean Save (Binary mode to prevent blank lines)
  raw_content = cal.serialize()
  lines = [line.strip() for line in raw_content.splitlines() if line.strip()]
  clean_content = "\r\n".join(lines) + "\r\n"

  with open(file_path, "wb") as f:
      f.write(clean_content.encode('utf-8'))

  print_separator()
  print(f"'{file_path}' sucessfully generated!")
  # Validator: https://icalendar.org/validator.html

except Exception:
    # traceback.format_exc() captures the full error stack trace
    error_details = traceback.format_exc()
    send_error_email("laerkevej_events.py", error_details)
    raise # Re-raises the error so the script still reports as failed