#!/usr/bin/env python
#
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
#

import arrow
from icalendar import Calendar, Event
from datetime import datetime
from dateutil import tz

def iter_months(start_year, num_years):
    '''
    Return a list of (month_start, month_end) for each month from the
    beginning of start_year spanning num_years years.
    '''
    start = arrow.get(datetime(start_year, 1, 1))
    end = start.replace(years=+num_years).ceil('year')
    return arrow.Arrow.span_range('month', start, end)

def iter_recycling_pickup_days(start_year, num_years):
    '''
    Yield Fridays of the second and fourth full weeks
    of each month from the beginning of start_year spanning
    num_years years.
    '''
    #TODO: handle holidays that offset recycling collection!
    for month_start, month_end in iter_months(start_year, num_years):
        # Expand the month to the first day of the first week and the last
        # day of the last week, since they may start and end outside of the
        # month.
        weeks = arrow.Arrow.range('week', month_start.floor('week'), month_end.ceil('week'))
        # Drop the first week if it's not a full week.
        if weeks[0] < month_start:
            weeks.pop(0)
        # Now yield Fridays on the second and fourth weeks,
        # since these are all full weeks.
        yield weeks[1].replace(days=+4)
        yield weeks[3].replace(days=+4)

def make_recycling_calendar(start_year, num_years):
    cal = Calendar()
    now = arrow.now()
    cal.add('prodid', '-//Recycling pickup generator//mielczarek.org//')
    cal.add('version', '1.0')
    for day in iter_recycling_pickup_days(start_year, num_years):
        event = Event()
        event.add('summary', 'Recycling Pickup')
        event.add('dtstart', day.date())
        event.add('dtend', day.replace(days=+1).date())
        event.add('dtstamp', now.datetime)
        cal.add_component(event)
    print cal.to_ical()

if __name__ == '__main__':
    make_recycling_calendar(arrow.now().year - 1, 2)
