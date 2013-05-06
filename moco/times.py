from time import localtime
from datetime import date, datetime, time, timedelta

Date = date
Time = time
TimeDelta = timedelta
Timestamp = datetime

def DateFromTicks(ticks):
    return Date(*localtime(ticks)[:3])

def TimeFromTicks(ticks):
    return Time(*localtime(ticks)[3:6])

def TimestampFromTicks(ticks):
    return Timestamp(*localtime(ticks)[:6])
