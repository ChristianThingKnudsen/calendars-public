from typing import TypedDict, List
from typing_extensions import NotRequired

class BirthdayEntry(TypedDict):
    date: str
    name: str
    number: int
    showBirthYear: NotRequired[bool]

birthdays: List[BirthdayEntry] = [
  {
    "date": "2024-01-02",
    "name": "Carl-Emil",
    "number": 3
  },
  {
    "date": "2026-01-18",
    "name": "Silke",
    "number": 1,
    "showBirthYear": True
  },
  {
    "date": "2024-02-09",
    "name": "Astrid",
    "number": 10
  },
  {
    "date": "1997-02-13",
    "name": "Cecilie",
    "number": 1,
    "showBirthYear": True
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
    "date": "1996-05-18",
    "name": "Christian",
    "number": 1,
    "showBirthYear": True
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

class EventEntry(TypedDict, total=False):
    name: str
    description: str
    start: str  # Format: "YYYY-MM-DD HH:MM"
    end: str    # Format: "YYYY-MM-DD HH:MM"

events: List[EventEntry] = [
    # {
    #     "name": "Vejfest7",
    #     "description": "Husk drikkevarer",
    #     "start": "2026-02-11 12:00",
    #     "end": "2026-02-11 23:59"
    # }
]