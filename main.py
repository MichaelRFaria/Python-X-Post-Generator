from tweet_cleaner import run_pipeline
from generator import generate_posts

run_pipeline("data/tweets.js", "data/clean_tweets.txt")
generate_posts("data/clean_tweets_no_mentions.txt")
