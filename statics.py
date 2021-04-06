class Statics:

    ROOT = ''

    ROOT_SCHEDULES = ROOT + 'schedule_pictures/'
    PATH_DAYS_JANUARY = ROOT_SCHEDULES + 'days_january.png'
    PATH_DAYS_FEBRUARY = ROOT_SCHEDULES + 'days_february.png'
    PATH_DAYS_MARCH = ROOT_SCHEDULES + 'days_march.png'
    PATH_SCHEDULE_1_15 = ROOT_SCHEDULES + 'schedule_1_15.png'
    PATH_SCHEDULE_1_15__2_HOUR_DELAY = ROOT_SCHEDULES + 'schedule_1_15__2_hour_delay.jpg'
    PATH_SCHEDULE_2_15 = ROOT_SCHEDULES + 'schedule_2_15.png'
    PATH_SCHEDULE_VIRTUAL_2_15 = ROOT_SCHEDULES + 'schedule_virtual_2_15.png'

    ROOT_DATA = ROOT + 'data/'
    PATH_CREDENTIALS = ROOT_DATA + 'credentials.json'
    PATH_PICKLE_EVENTS = ROOT_DATA + 'events.p'
    PATH_PICKLE_TOKEN = ROOT_DATA + 'token.pickle'
    PATH_PICKLE_SYED = ROOT_DATA + 'syed_messed_up.p'
    PATH_TXT_SYED = ROOT_DATA + 'syed_messed_up.txt'

    SERVER_ID = 761272774719176745

    CHANNEL_GENERAL = 761272775310180386
    CHANNEL_BELL_RING = 761273344054001675
    CHANNEL_OPT_IN = 780834981139709962
    CHANNEL_COMMANDS = 778298409077309441
    CHANNEL_PICKLES = 761568872813297694
    CHANNEL_THE_RULES = 763176541009608745
    CHANNEL_SOLITAIRE = 763494119137738783
    CHANNEL_ATTENDANCE = 778250365208494081

    ROLES = {
        "COUNCIL_ROCK": 761549395115900939,
        "PERIOD_1": 780556664533024779,
        "PERIOD_2": 780834551986388993,
        "PERIOD_3": 780834581704212581,
        # "PERIOD_4" : 780834611201835068,
        # "PERIOD_5" : 780834635156029491,
        # "PERIOD_6" : 780834656111165460,
        # "PERIOD_7" : 780834702939783181,
        # "PERIOD_8" : 780834736666837002,
        "PERIOD_9": 780834775036198942,
        "PERIOD_4_5_6": 783730555018805329,
        "PERIOD_6_7_8": 783730611155501137
    }

    CALENDAR_EVENTS = {
        "Period 1": "PERIOD_1",
        "Period 2": "PERIOD_2",
        "Period 3": "PERIOD_3",
        # "Period 4": "PERIOD_4",
        # "Period 5": "PERIOD_5",
        # "Period 6": "PERIOD_6",
        # "Period 7": "PERIOD_7",
        # "Period 8": "PERIOD_8",
        "Period 9": "PERIOD_9",
        "Period 4/5/6": "PERIOD_4_5_6",
        "Period 6/7/8": "PERIOD_6_7_8"
    }

    MESSAGES = {
        "PERIOD_1": 804746380491882556,
        "PERIOD_2": 804746390831628288,
        "PERIOD_3": 804746396405465088,
        "PERIOD_4_5_6": 804746404471111681,
        "PERIOD_6_7_8": 804746417305419817,
        "PERIOD_9": 804746430613815296
    }

    DAYS_OF_WEEK = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    MONTHS = [
        "<error>",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ]

    ROLE_EVERYONE = 761272774719176745
