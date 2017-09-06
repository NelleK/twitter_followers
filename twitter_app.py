# This script writes new followers and unfollewers to the console
import tweepy
import itertools
import csv
import os.path
import schedule as sch
import time
from shutil import move

# testing git push and pull to github and bitbucket
# test commit 1

def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page

def setup_api():
    # @nellekooren app keys
    # opens the file and automatically closes upon dedentation, with read and Unicode
    # as f defines f as file handler variable
    with open('/home/nelle/.twitter_keys', 'rU') as f:
        # creates a list with lists for each line by .split('='),
        # containing keyname and password
        # and then creates a dictionary with keyname as key and passw as value
        twitter_keys = dict(line.strip().split('=') for line in f)
    consumer_key = twitter_keys.get('consumer_key', '')
    consumer_secret = twitter_keys.get('consumer_secret', '')
    access_token = twitter_keys.get('access_token', '')
    access_token_secret = twitter_keys.get('access_token_secret', '')
    # Creating an OAuthHandler instance.
    # Into this we pass our consumer token and secret.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Creation of the actual interface, using authentication
    # Caches what's done in last 60 minutes
    return tweepy.API(auth)
    #cache=tweepy.FileCache('cache', timeout=60*60))

# putting the interface into a variable
api = setup_api()

def write_outfollowers_1():
    # puts in a variable the user ids of followers at the time when function is run
    followers = api.followers_ids(screen_name='daysofcode')
    # creates and opens csv
    with open('followers_user_1.csv', 'w') as f:
        # Puts into variable writer a writer object responsible for converting
        # the user’s data into delimited strings on the given file-like object/
        writer = csv.writer(f, dialect='excel')
        # calls pagination function on variable followers and loops over pages
        for page in paginate(follower, 100):
            # stores the user information for each follower on each page in results
            results_1 = api.lookup_users(user_ids=page)
            # assigns to outfollowers a list of the followers
            # with for each follower a list containing screen_name and id
            # looping over the information per user in results
            outfollowers_1 = [[info.screen_name, info.id] for info in results_1]
            # writes results into the opened csv file
            # writes the list to the writer’s file object; ie the csv file
            writer.writerows(outfollowers_1)
        return outfollowers_1

def write_outfollowers_2():
    # puts in a variable the user ids of followers at time when function is run
    followers = api.followers_ids(screen_name='daysofcode')
    with open('followers_user_1.csv', 'r') as f:
        # creates the reader object to read over the file
        reader = csv.reader(f)
        outfollowers_2 = list(reader)
    with open('tempfile.csv', 'w') as f:
        writer = csv.writer(f, dialect='excel')
        # calls pagination function on variable followers and loops over pages
        for page in paginate(followers, 100):
            # stores the user information for each follower on each page in results
            results = api.lookup_users(user_ids=page)
            # interates over the information in results
            # taking for each follower the screen name and the id
            # puts that as a list of lists [<screen_name>, <id>] in outfollowers_2
            outfollowers_1 = [[info.screen_name, str(info.id)] for info in results]
            # writes each list in outfollowers_2 to the csv file
            # writes results into the opened csv file
            # writes the list to the writer’s file object; ie the csv file
            writer.writerows(outfollowers_1)
            return(outfollowers_1, outfollowers_2)

def move_file(src, dest):
    move(src, dest)

def compare_followers(newlist, oldlist):
    # turns the ids - name pairs into tuples with map
    # sorts the list and makes a set out of it with the purpose of comparison
    newlist_s = set(sorted(map(tuple, newlist)))
    oldlist_s = set(sorted(map(tuple, oldlist)))
    unfollowers =  oldlist_s - newlist_s
    new_followers = newlist_s - oldlist_s
    print("These are your unfollowers: \n", unfollowers)
    print("These are your new followers: \n", new_followers)
    return unfollowers

def get_started():
    # checks if csv file exists, if it doesn't, it runs the function to create it.
    if not os.path.isfile('/home/nelle/pythonpract/followers_user_1.csv'):
        write_outfollowers_1()
    else:
        # assigns the follower lists from the tuple returned to write_outfollowers_2 to
        # variables followers_1 and followers_2
        followers_1, followers_2 = write_outfollowers_2()
        move_file('tempfile.csv', 'followers_user_1.csv')
        ##print(followers_1, followers_2)
        # calls compare_followers with the follower lists as argumensts
        # then calls unfollow with the unfollowers as an argument (returned by compare_followers)
        unfollowers = compare_followers(followers_1, followers_2)
        ##print(unfollowers)
        ## unfollow(unfollowers)

def morning():
    # schedules running get_started every x seconds
    sch.every(2).seconds.do(get_started)

    while 1:
        # runs all jobs pending to run
        try:
            sch.run_pending()
            # suspends execution for 1 second
            time.sleep(1)
        except:
            continue
        # break

morning()
