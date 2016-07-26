#!/usr/bin/env python
#
# Any copyright is dedicated to the Public Domain.
# http://creativecommons.org/publicdomain/zero/1.0/
#

import datetime
from genrecyclingcalendar import make_recycling_calendar

ONE_YEAR = int(datetime.timedelta(365).total_seconds())

def application(env, start_response):
    start_response('200 OK',
                   [
                       ('Content-Type', 'text/calendar'),
                       ('Cache-Control', 'max-age=%d' % ONE_YEAR),
                       ('Access-Control-Allow-Origin', '*'),
                   ])
    return [make_recycling_calendar()]
