import tweepy
import time
from termcolor import colored, cprint

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''


def login(consumer_key, consumer_secret, access_token, access_token_secret):

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth)



# DELETE ACCORDING TO PRESET RULES AND SCORING
def delete(api, allow, deny):
    print("You are about to DELETE TWEETS using preset rules from @" +
          api.verify_credentials().screen_name)
    deleted = 0
    total = 0
    for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended').items():
        total = total + 1

        # reset score for every tweet
        keep = 0

        # score normal tweets
        if not hasattr(status, 'retweeted_status'):

            content = status.full_text
            content = content.encode('ascii', errors='replace').decode('ascii')
            content = content.lower()

            if any(ext in content for ext in deny):
                keep = 0
            else:
                if any(ext in content for ext in allow):
                    keep = 2
                elif status.favorited:
                    keep = 1
                elif status.retweet_count > 0:
                    keep = 1
                elif status.favorite_count > 0:
                    keep = 1
        # score retweets
        else:
            content = status.retweeted_status.full_text
            content = content.encode('ascii', errors='replace').decode('ascii')
            content = content.lower()

            if any(ext in content for ext in deny):
                keep = 0
            else:
                if any(ext in content for ext in allow):
                    keep = 2
                elif status.favorited:
                    keep = 1
                elif status.retweeted_status.favorited:
                    keep = 1
        # printing and deleting
        if keep == 0:
            api.destroy_status(status.id)
            cprint(status.full_text, 'red')
            deleted += 1
            time.sleep(0.3)
        elif keep == 2:
            cprint(status.full_text, 'green')
        elif keep == 1:
            cprint(status.full_text, 'cyan')

    print("Total: ", str(total))
    print("Total deleted: ", str(deleted))


# DELETE EVERYTHING TIL' THE API LIMIT *may required another run*
def delete_all(api):
    print("You are about DELETE ALL tweets from@" +
          api.verify_credentials().screen_name)
    deleted = 0
    total = 0
    for status in tweepy.Cursor(api.user_timeline, tweet_mode='extended').items():
        total = total + 1
        api.destroy_status(status.id)
        cprint(status.full_text, 'red')
        deleted += 1
        time.sleep(0.1)

    print("Total: ", str(total))
    print("Total deleted: ", str(deleted))

# DELETE FAVS/LIKES
def delete_favs(api):
    print("You are about UNLIKE ALL tweets from @" +
          api.verify_credentials().screen_name)
    deleted = 0
    total = 0
    for status in tweepy.Cursor(api.favorites).items():
        total = total + 1
        api.destroy_favorite(status.id)
        cprint(str(deleted), 'red')
        deleted += 1
        time.sleep(0.1)

    print("Total: ", str(total))
    print("Total favs deleted: ", str(deleted))

# LIST FOLLOWERS
def list_followers(api, username):

    screen_name = username
    print("### FOLLOWERS ##")
    for f in tweepy.Cursor(api.followers, screen_name).items():

        print(f.screen_name)

        time.sleep(1)

# LIST FRIENDS
def list_friends(api, username):

    screen_name = username
    print("### FOLLOWS ##")
    for f in tweepy.Cursor(api.friends, screen_name).items():

        print(f.screen_name)

        time.sleep(5)


if __name__ == "__main__":
    api = login(CONSUMER_KEY, CONSUMER_SECRET,
                ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    print('Authenticated as: ' + api.me().screen_name)
    # list of words that allow to bypass deleting
    allow = []
    # list of words that force deleting
    deny = []

    delete(api, allow, deny)
