import praw, time, tweepy, json, requests, os 
from datetime import datetime

# For reading the variables from the config
with open('config.json') as f: config = json.load(f)

# Initialize the reddit instance
reddit = config['reddit']
r = praw.Reddit(
    client_id= reddit['client_id'],
    client_secret= reddit['client_secret'],
    password= reddit['password'],
    user_agent= reddit['user_agent'],
    username= reddit['username']
)

# Initialize the twitter instance
twitter = config['twitter']
auth = tweepy.OAuthHandler(twitter['consumer_key'], twitter['consumer_secret'])
auth.set_access_token(twitter['access_token'], twitter['access_token_secret'])
api = tweepy.API(auth)

# Infinite loop to keep sending them messages
while True:
    # Gets random subreddit
    subreddit = r.random_subreddit(nsfw=False)
    
    # Get the top post from the subreddit
    for topPost in subreddit.top(limit=25):
        
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        # check if the post has a picture
        if topPost.url.endswith('.jpg') or topPost.url.endswith('.png'):
            filename = 'temp.jpg'
            # Downloading the image
            request = requests.get(topPost.url, stream=True)
            if request.status_code == 200:
                with open(filename, 'wb') as image:
                    for chunk in request:
                        image.write(chunk)
                
                # Preparing the message
                tweetContent = topPost.title + '\nCredits: ' + 'reddit.com' + topPost.permalink
                
                # Just for future checking purposes
                print(current_time + ' ----------------------------------------------------------')
                print(current_time + ' Found a post from ' + subreddit.display_name)
                print(current_time + ' ' + tweetContent)
                print(current_time + ' ----------------------------------------------------------')
                
                # Post this tweet
                api.update_status_with_media(tweetContent, filename)
                
                # Deleting the file
                os.remove(filename)
            else:
                print("Unable to download image")
            break
        else:
            # Preparing the message
            tweetContent = topPost.title + '\nCredits: ' + 'reddit.com' + topPost.permalink
            
            # Just for future checking purposes
            print(current_time + ' ----------------------------------------------------------')
            print(current_time + ' Found a post from ' + subreddit.display_name)
            print(current_time + ' ' + tweetContent.replace('\n', ' | '))
            print(current_time + ' ----------------------------------------------------------')
            
            # Post this tweet
            api.update_status(tweetContent)
            break
            
    # Sleeping for an hour
    time.sleep(60 * 60)