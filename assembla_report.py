# -*- coding: utf-8 *-*
from assembla.models import *
from assembla.auth import assembla_auth, sendgrid_auth
import sendgrid
from datetime import datetime, timedelta
from dateutil import tz
from dateutil.parser import parse


def main():
    s = sendgrid.Sendgrid(sendgrid_auth[0], sendgrid_auth[1], secure=True)

    # Retrieve the Stream Events.
    # These are similar to those appearing on http://www.assembla.com/start (right side)

    api = API(assembla_auth, use_cache=False)
    events = api.events()
    spaces = api.spaces()
    local_zone = tz.tzlocal()

    # Retrieve the events happened in all spaces for an Organization, for a day.

    tday = datetime.now()
    tday = tday.replace(tzinfo=local_zone)
    this_day = (tday - timedelta(hours=24)).date()
    subject = "Agiliq-Assembla Summary for the day " + tday.strftime("%b %d %Y")
    plain_body = ""
    colors = {'funderhub': 'cyan', 'Occasio': 'green', 'TexStar University': 'brown'}

    for event in events:
        edt = parse(event.date)
        event_date_time = edt.astimezone(local_zone)
        event_date = event_date_time.date()
        if not event_date > this_day:
            break
        for space in spaces:
            for user in space.users():
                if user.id == event.author['id'] and event.space['id'] == space.id:
                    plain_body += "<br/> <hr/> <b>{0}</b> {1} @ <font color=".format(
                        event_date_time.strftime("%H:%M"),
                        event.author['name']
                        ) + \
                    colors[space.name] + ">{0}</font> <a href='{3}'>{1}</a> <br/> {2} <br/>".format(
                        space.name,
                        event.operation,
                        event.title,
                        event.url,
                        #event.whatchanged,
                        #event.comment_or_description,
                        )
                    if event.object == 'Ticket' and event.operation != 'created':
                        if getattr(event, 'whatchanged', None):
                            plain_body += "<font color='violet'>" + event.whatchanged + "</font><br/>"
                        elif getattr(event, 'comment_or_description', None):
                            plain_body += "<font color='violet'>" + event.comment_or_description + "</font><br/>"

    message = sendgrid.Message("ramana@agiliq.com", subject, "", "<div>" + plain_body + "</div>")
    message.add_to("ramana@agiliq.com", "Agilq Team")
    s.smtp.send(message)


if __name__ == '__main__':
    main()
