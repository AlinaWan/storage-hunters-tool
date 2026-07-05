from datetime import datetime
from typing import final as sealed

@sealed
class DateTimeUtil:
    @staticmethod
    def get_greeting():
        hour = datetime.now().hour

        if 5 <= hour < 12:
            return "Good morning"
        elif 12 <= hour < 18:
            return "Good afternoon"
        elif 18 <= hour < 22:
            return "Good evening"
        else:
            return "Good night"
