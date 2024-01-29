from .exceptions import TiktokException
from datetime import datetime, timedelta
from dateutil import parser
import pytz

def validate_participant_interactions(data):
    if 'video_id' not in data:
        raise TiktokException("Video Id is an required field")
    elif 'session_id' not in data:
        raise TiktokException("Session Id is an required field")
    elif 'start_time' not in data:
        raise TiktokException("Start Time is an required field")
    elif 'end_time' not in data:
        raise TiktokException("End Time is an required field")
    elif 'is_liked' not in data:
        raise TiktokException("Like status is an required field")

def check_is_session_exists (session_data):
    print(session_data)
    if not session_data[1]:
        raise TiktokException("Session already completed")

def current_time(minutes):
    current_timestamp = datetime.now() + timedelta(minutes = minutes)
    formatted_timestamp = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_timestamp

def unix_to_datetime(timestamp):
    if isinstance(timestamp, str):
        try:
            # Try to convert the input string to a int (Unix timestamp)
            unix_timestamp = int(timestamp)
            formatted_date = datetime.utcfromtimestamp(unix_timestamp)
        except ValueError:
            try:
                # Try to parse the input string as a datetime
                formatted_date = parser.parse(timestamp)
            except ValueError:
                raise TiktokException("Invalid date input. Please provide a valid date.")
    elif isinstance(timestamp, (int, float)):
        # Input is a Unix timestamp (assumed to be in seconds)
        formatted_date = datetime.utcfromtimestamp(int(timestamp))
    else:
        formatted_date = parser.parse(timestamp)
    timezone = pytz.timezone('America/New_York')
    formatted_date = timezone.localize(formatted_date)
    return formatted_date
