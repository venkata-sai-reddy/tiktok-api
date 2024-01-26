from .exceptions import TiktokException
from datetime import datetime, timedelta

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

def unix_to_datetime(unix_timestamp):
    time_format = datetime.utcfromtimestamp(int(unix_timestamp))
    return time_format.strftime('%Y-%m-%d %H:%M:%S')
