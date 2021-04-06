from __future__ import print_function
from datetime import datetime, timedelta
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from statics import Statics
import requests, json

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Calendar:

    @staticmethod
    def getEventsFromGoogle():
        """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(Statics.PATH_PICKLE_TOKEN):
            with open(Statics.PATH_PICKLE_TOKEN, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    Statics.PATH_CREDENTIALS, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(Statics.PATH_PICKLE_TOKEN, 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=None, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        pickle.dump(events, open(Statics.PATH_PICKLE_EVENTS, "wb"))

        offset = 0
        with open("data/cr_offset.txt", "r") as f:
            offset = int(f.read())

        events_website = []
        for event in events:
            if 'dateTime' in event['start']:
                events_website.append(["period", event['summary'].split(' ')[1], Calendar.parse_time(event['start']['dateTime']).timestamp() + offset,
                                       Calendar.parse_time(event['end']['dateTime']).timestamp() + offset])
            elif 'Day' in event['summary']:
                events_website.append(["day", event['summary'].split(' ')[1], Calendar.parse_date(event['start']['date']).timestamp(),
                                       Calendar.parse_date(event['start']['date']).timestamp() + (3600*24)])
        requests.post("", data={'events': json.dumps(events_website)})

    @staticmethod
    def getEvents():
        string_events = ""
        for event in pickle.load(open(Statics.PATH_PICKLE_EVENTS, "rb")):
            start = event['start']['dateTime']
            start_time = Calendar.parse_time(start)
            string_events += str(start_time) + ": " + event['summary'] + "\n"
        return string_events

    @staticmethod
    def getEventsList():
        return pickle.load(open(Statics.PATH_PICKLE_EVENTS, "rb"))

    @staticmethod
    def next_period():
        events = Calendar.getEventsList()
        for event1 in events:
            if 'dateTime' in event1['start']:
                event = Calendar.parse_time(event1['start']['dateTime'])
                seconds_until_event = Calendar.get_seconds_until(event)
                if 'Period' in event1['summary'] and seconds_until_event > 0:
                    hours, remainder = divmod(seconds_until_event, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    ret_str = 'Next period, ' + event1['summary'] + ', is in'
                    if hours > 0:
                        ret_str += " {:02} hour".format(int(hours))
                        if hours > 1:
                            ret_str += "s"
                        if minutes > 0:
                            ret_str += ", {:02} minute".format(int(minutes))
                            if minutes > 1:
                                ret_str += "s"
                            ret_str += ", and {:02} second".format(int(seconds))
                            if seconds > 1:
                                ret_str += "s"
                            ret_str += ","
                        else:
                            ret_str += " and {:02} second".format(int(seconds))
                            if seconds > 1:
                                ret_str += "s"
                            ret_str += ","
                    else:
                        if minutes > 0:
                            ret_str += " {:02} minute".format(int(minutes))
                            if minutes > 1:
                                ret_str += "s"
                            ret_str += " and {:02} second".format(int(seconds))
                            if seconds > 1:
                                ret_str += "s"
                            ret_str += ","
                        else:
                            ret_str += " {:02} second".format(int(seconds))
                            if seconds > 1:
                                ret_str += "s"
                            ret_str += ","
                    display_hour = event.hour % 12
                    if display_hour == 0:
                        display_hour = 12
                    strminute = str(event.minute)
                    if (len(strminute) == 1):
                        strminute = "0" + strminute
                    ret_str += ' at ' + str(display_hour) + ':' + strminute + ("am." if event.hour < 12 else "pm.")
                    return ret_str

    @staticmethod
    def time_until_next_period():
        events = Calendar.getEventsList()
        for event1 in events:
            if 'dateTime' in event1['start']:
                event = Calendar.parse_time(event1['start']['dateTime'])
                seconds_until = Calendar.get_seconds_until(event)
                if 'Period' in event1['summary'] and seconds_until > 0:
                    return seconds_until
        print('no events?')

    @staticmethod
    def next_period_json():
        events = Calendar.getEventsList()
        for event1 in events:
            if 'dateTime' in event1['start']:
                event = Calendar.parse_time(event1['start']['dateTime'])
                if 'Period' in event1['summary'] and Calendar.get_seconds_until(event) > 0:
                    return event1

    @staticmethod
    def get_day():
        events = Calendar.getEventsList()
        for event1 in events:
            if 'date' in event1['start']:
                event = Calendar.parse_date(event1['start']['date'])
                if 'Day ' in event1['summary'] and -24 * 60 * 60 < Calendar.get_seconds_until(event) < 0:
                    return event1['summary'][4:]
        return None

    @staticmethod
    def get_cohort():
        events = Calendar.getEventsList()
        for event1 in events:
            if 'date' in event1['start']:
                event = Calendar.parse_date(event1['start']['date'])
                if 'Cohort ' in event1['summary'] and 0 < Calendar.get_seconds_until(event) < 24 * 60 * 60:
                    return event1['summary'][7:]
        return None

    @staticmethod
    def parse_time(x):
        return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S-04:00')

    @staticmethod
    def parse_date(x):
        return datetime.strptime(x, '%Y-%m-%d')

    @staticmethod
    def get_seconds_until(event):

        offset = 0
        with open("data/cr_offset.txt", "r") as f:
            offset = int(f.read())

        now = datetime.utcnow() - timedelta(hours=4) - timedelta(seconds=offset)
        return (event - now).total_seconds()
