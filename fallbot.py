import random
import tweepy

from pytz import timezone, utc

from time import sleep

from datetime import datetime, timedelta, date

CONSUMER_KEY = 'eMVZBpgEJ75JC1xyNyzVQ6sO4'
CONSUMER_SECRET = 'kuluz9Wrc8U6hfOOoSafGtsWf6tUAojL1sQjyH5BNPkdIjqlen'
ACCESS_TOKEN = '897666750640029697-UjxY6VOGjLDTkjRCT9So87bUrzzilR6'
ACCESS_TOKEN_SECRET = 'Bss1XKBoRq8LWW6n9zDLYKSQirBeBel0fSZoKNP7pDXpR'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


"""
setting this as the constant for TAPI
"""
TAPI = tweepy.API(auth)

###
PHRASE_BOOK = [
    'Fall starts in {}',
    'Days till fall: {}',
    'My favorite season starts in {}',
    'No pumpkin spice lattes for the next {}',
    'I cant wait to drink a hot toddy in {}',
    'FML for the next {}',
    'Leaves start changing color in {}',
    'We only have to wait {} until fall',
    'The best season starts in {}',
    "Hey guys Fall here, I'm coming for you in {}",
]
# FALL_START = datetime(2021, 9, 22)
SUMMER_START_DAY = 170
FALL_START_DAY = 265

LAST_RUN_LOG_FILE = '/Users/Kirsten/Desktop/KIRSTEN/last_run.log'

### Check if ran today - if false then maybe we should run
def ran_today():
    try:
        with open(LAST_RUN_LOG_FILE, 'r') as f:
            datestring = f.readlines()[0].rstrip()
            d = datetime.strptime(datestring, "%Y-%m-%d").date()
            if datetime.now().date() == d:
                return True
            return False
    except IOError:
        print("File not found so running for first time.")
        return False

### logging if ran
def log_today():
    with open(LAST_RUN_LOG_FILE, 'w') as f:
        f.write(str(datetime.now().date()))

def get_time_till_fall():
    now = datetime.now()
    fall_start = datetime(now.year, 1, 1) + timedelta(FALL_START_DAY - 1)

    d = fall_start - now
    # string formatting to make it look good
    d = str(d).split('.')[0] # remove miliseconds
    s = d.split(':')
    d = "%s hours, %s minutes and %s seconds" % (s[0], s[1], s[2])
    return d

def randomize_day():
    """
        I enjoyed this problem, how to randomize the post throughout the day.
        When the program runs - it takes the number of seconds that have passed today
        and a random number between 0 and total number of seconds in a day.
        If the random number is lower than the number of seconds passed in a day, then we posting for the day.
        We could normalize this but I like what we've got so far.
        Ex: Chance to run at midnight, very low, chance to run at noon 50%, chance to run at 11:59pm 100%.
    """
    seconds_in_day = 86400
    n = datetime.now()
    seconds_today = n.hour * 3600 + n.minute * 60 + n.second
    #if seconds_today < 32400
        #return False
    r = int(random.random() * 86400)
    if r < seconds_today:
        # sleep for a random 6 hours to hide the fact it runs on 6 hour interval
        sleep(random.random() * 300)
        return True
    return False

def post_to_twitter():
    p = random.choice(PHRASE_BOOK).format(get_time_till_fall())
    print (p)
    TAPI.update_status(status=p)

def run():
    doy = datetime.today().timetuple().tm_yday
    if doy == FALL_START_DAY:
        if not ran_today() and randomize_day():
            msg = "IT'S FALL"
            TAPI.update_status(status=msg)
            log_today()
    if doy > SUMMER_START_DAY and doy < FALL_START_DAY:
        if not ran_today() and randomize_day(): #makes the time bot tweets seem "random"
            post_to_twitter()
            log_today()

            
if __name__ == "__main__":
    """
    We assume crontab is run every 5 minutes
    """
    run()
