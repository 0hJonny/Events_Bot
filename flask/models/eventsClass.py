from dataclasses import dataclass, field

@dataclass
class Event:
    object: str
    municipality: str
    event_name: str
    event_date: str
    event_address: str