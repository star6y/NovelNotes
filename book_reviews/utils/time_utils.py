from dateutil.tz import tzlocal
from dateutil import tz

def utc_to_local_timezone_string(utc_timestamp):
    # central time
    to_zone = tz.gettz('America/Chicago')
    from_zone = tz.gettz('UTC')
    utc_timestamp = utc_timestamp.replace(tzinfo=from_zone)
    local_timestamp = utc_timestamp.astimezone(to_zone)
    return local_timestamp.strftime("%B %d, %I:%M %p")
