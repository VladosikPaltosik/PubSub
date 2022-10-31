from pydantic import BaseModel


class Recording(BaseModel):
    vehicle_id: str
    signals: dict
