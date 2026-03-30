import uuid
from datetime import datetime, timezone, date
from typing import Union

class Utils:
    @staticmethod
    def get_now_iso():
        # Returns current UTC time as string with 'Z' suffix
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def date_to_iso(date_obj: Union[date, datetime]):
        # Handles both date (YYYY-MM-DD) and datetime objects
        if isinstance(date_obj, datetime):
            return date_obj.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
        
        # If it's just a date, combine with min time (00:00:00)
        return datetime.combine(date_obj, datetime.min.time()).replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")

    @staticmethod
    def generate_fid():
        return str(uuid.uuid4())