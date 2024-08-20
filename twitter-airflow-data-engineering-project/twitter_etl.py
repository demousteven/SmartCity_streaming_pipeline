import tweepy  # Twitter API library for interacting with Twitter data
import pandas as pd  # Library for data manipulation and analysis

def run_twitter_etl():
    # Define your Twitter API credentials
    access_key = "714230983-Mbr3vHM9LebHXzlXo7gBT6UgTFtqT1EkarV9beGa"
    access_secret = "KAyG3mFNz7VkrSfPbNhij4zdD4Gb2xb4nPE2jc4MaZNuN"
    consumer_key = "NrS45iCByMQqMlXNQdTENvEub"
    consumer_secret = "ZlUIMW1UB8XmZHWPcs3ElkUL12SAAGyKPn2OvUvDHoBcuntKVlacces"

    # Authenticate with Twitter API using the credentials
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # Create an API object with rate limit handling
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # Fetch tweets from the specified user timeline
    tweets = api.user_timeline(
        screen_name='elonmusk',  # Twitter handle of the user (no '@' needed)
        count=200,               # Number of tweets to fetch
        include_rts=False,       # Exclude retweets
        tweet_mode='extended'    # Fetch full text of tweets
    )

    # List to store refined tweet data
    tweet_list = []
    for tweet in tweets:
        text = tweet.full_text  # Get the full text of the tweet

        # Create a dictionary with relevant tweet details
        refined_tweet = {
            "user": tweet.user.screen_name,  # Username of the tweet author
            "text": text,                    # Full text of the tweet
            "favorite_count": tweet.favorite_count,  # Number of likes
            "retweet_count": tweet.retweet_count,    # Number of retweets
            "created_at": tweet.created_at         # Timestamp of the tweet
        }

        # Append the refined tweet data to the list
        tweet_list.append(refined_tweet)

    # Convert the list of tweets to a pandas DataFrame
    df = pd.DataFrame(tweet_list)

    # Save the DataFrame to a CSV file
    df.to_csv('refined_tweets.csv', index=False)

# Run the ETL function if this script is executed directly
if __name__ == "__main__":
    run_twitter_etl()
