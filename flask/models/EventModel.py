from typing import List, Optional
from pydantic import BaseModel


class Cells(BaseModel):
    NAIMENOVANIE_MEROPRIYATIYA_V_SOOTVETSTVI: str
    SROKI_PROVEDENIYA: str
    MESTO_PROVEDENIYA: str
    UCHASTNIKI_MEROPRIYATIYA_: str
    ORGANIZATOR_MEROPRIYATIYA: str


class Items(BaseModel):
    Number: int
    Cells: Cells


# Use the class
class EventModel(BaseModel):
    name: str
    totalCount: int
    Count: int
    Items: List[Items]