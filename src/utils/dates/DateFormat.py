import datetime

class DateFormat():

    @classmethod
    def format_date(cls, date):
        return datetime.datetime.strftime(date, "%d/%m/%Y")
    
    @classmethod
    def from_string(cls, value):
        try:
            return datetime.datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Invalid date format, must be: dd/mm/yyyy")