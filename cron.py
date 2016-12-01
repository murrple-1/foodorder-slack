import re

class CronScheduleTime:
    MIN_RANGE = range(0, 60)
    HOUR_RANGE = range(0, 24)
    DAY_OF_MONTH_RANGE = range(1, 32)
    MONTH_RANGE = range(1, 13)
    DAY_OF_WEEK_RANGE = range(0, 7)

    def __init__(self, minute, hour, day_of_month, month, day_of_week):
        if minute is not None and minute not in self.MIN_RANGE:
            raise TypeError('minute malformed')

        if hour is not None and hour not in self.HOUR_RANGE:
            raise TypeError('hour malformed')

        if day_of_month is not None and day_of_month not in self.DAY_OF_MONTH_RANGE:
            raise TypeError('day_of_month malformed')

        if month is not None and month not in self.MONTH_RANGE:
            raise TypeError('month malformed')

        if day_of_week is not None and day_of_week not in self.DAY_OF_WEEK_RANGE:
            if day_of_week == 7:
                day_of_week = 0
            else:
                raise TypeError('day_of_week malformed')

        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week

    def __str__(self):
        minute = self.minute if self.minute is not None else '*'
        hour = self.hour if self.hour is not None else '*'
        day_of_month = self.day_of_month if self.day_of_month is not None else '*'
        month = self.month if self.month is not None else '*'
        day_of_week = self.day_of_week if self.day_of_week is not None else '*'

        return '{0} {1} {2} {3} {4}'.format(minute, hour, day_of_month, month, day_of_week)

    def isOn(self, dt):
        date = dt.date()
        time = dt.time()

        if self.minute is not None:
            if self.minute != time.minute:
                return False

        if self.hour is not None:
            if self.hour != time.hour:
                return False

        if self.day_of_month is not None:
            if self.day_of_month != date.day:
                return False

        if self.month is not None:
            if self.month != date.month:
                return False

        if self.day_of_week is not None:
            if self.day_of_week != date.weekday():
                return False

        return True

_prog = None
def parseCronSchedule(cronSchedule):
    global _prog
    if not _prog:
        _prog = re.compile(r'^(\*|\d{1,2}) (\*|\d{1,2}) (\*|\d{1,2}) (\*|\d{1,2}) (\*|\d)$')

    matchObj = _prog.match(cronSchedule)

    if not matchObj:
        raise ValueError('malformed cron schedule text')

    minute = matchObj.group(1)
    hour = matchObj.group(2)
    day_of_month = matchObj.group(3)
    month = matchObj.group(4)
    day_of_week = matchObj.group(5)

    if minute == '*':
        minute = None
    else:
        minute = int(minute)

    if hour == '*':
        hour = None
    else:
        hour = int(hour)

    if day_of_month == '*':
        day_of_month = None
    else:
        day_of_month = int(day_of_month)

    if month == '*':
        month = None
    else:
        month = int(month)

    if day_of_week == '*':
        day_of_week = None
    else:
        day_of_week = int(day_of_week)

    return CronScheduleTime(minute, hour, day_of_month, month, day_of_week)
