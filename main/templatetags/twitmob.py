from django import template

import datetime 
from django.utils import dateformat
from django.utils import timezone


register = template.Library()


@register.simple_tag
def diff_date(date, limen=2):
    if not date:
        return ('unknown')

    now = timezone.now()
    # print now
    # date =  date.replace(tzinfo=None)

    diff = date - now 

    hours = int(diff.seconds/3600)
    minutes = int(diff.seconds/60)
    days = int(diff.total_seconds()/86400)
    # print days

    if diff.total_seconds()  > 0:
        if date.year != now.year:
            return "starts on " +dateformat.format(date, 'd M \'y, H:i')
        elif days > 2:
            return "starts on " + dateformat.format(date, 'd M, H:i')

        elif days == 2:
            return 'starts in 2 days'
        elif days == 1:
            return 'starts tomorrow'
        elif minutes >= 60:
            if hours == 1:
                return ('starts in %(hr)d ' + "hour") % {'hr':hours}
            else: 
                return ('starts in %(hr)d ' + "hours") % {'hr':hours}
        elif diff.seconds >= 60:
            if diff.seconds == 60:
                return ('starts in %(min)d ' + "min") % {'min':minutes} 
            else:
                return ('starts in %(min)d ' + "mins") % {'min':minutes}
        else:
            if diff.seconds == 1:
                return ('starts in %(sec)d ' + "sec") % {'sec':diff.seconds}
            else:
                return ( 'starts in %(sec)d ' + "secs") % {'sec':diff.seconds}
    else:
        minutes = (diff.total_seconds() * -1 ) / 60
        return ('ends in %(min)d min' ) % {'min':60-minutes} 
