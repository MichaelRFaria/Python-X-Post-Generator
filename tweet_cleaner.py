import json
import re
from collections import defaultdict
from collections.abc import Callable
from math import floor
from statistics import mean
import os.path

# loads the given JS file of tweets
def load_raw_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f: # utf-8 encoding for emojis, etc
        return f.read()

# extracts tweets from raw JSON data and converts to Python dictionary
def extract_tweets_json(raw: str):
    # remove "window.YTD.tweets.part0 = " from text
    json_data = raw.split("=", 1)[1].strip()

    # convert JSON to Python dictionary
    return json.loads(json_data)

# tweet preprocessing
def clean_tweet_text(text: str, cleaning_criteria: str) -> str:
    text = re.sub(r"https://t\.co/\S+", "", text)

    # remove newlines, normalise whitespaces, remove leading and trailing linespaces
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text.strip()

    #print(text)
    #print(repr(text))

    match cleaning_criteria:
        case "normal":
            # if the remaining tweet is just a mention(s), then skip it
            if re.match(r"^(@\w+\s*)+$", text):
                return ""
        case "no_replies":
            # if the tweet is a mention, then skip it
            if re.match(r"@+", text):
                return ""

    # skip empty tweets
    if text == "" or text == " ":  # todo - previous strip should mean that text == " " isn't needed, but for some reason it is necessary
        return ""

    return text

# preprocesses all given tweets as a list (for a text file)
def process_tweets_to_list(raw: str, cleaning_criteria: str) -> list[str]:
    tweets_data = extract_tweets_json(raw)

    tweets = []

    for item in tweets_data:
        tweet = item["tweet"]

        text = tweet.get("full_text", "")

        cleaned_text = clean_tweet_text(text, cleaning_criteria)

        if cleaned_text == "":
            continue

        tweets.append(cleaned_text)

    return tweets

# preprocesses all given tweets as a dictionary (for a json file)
# currently saves tweets with their number of likes. this will have some sort of condiitonal/branching in the future for alternate scenarios.
def process_tweets_to_dict(raw: str) -> dict:
    tweets_data = extract_tweets_json(raw)

    tweets = defaultdict(list[int])

    for item in tweets_data:
        tweet = item["tweet"]

        text = tweet.get("full_text", "")

        cleaned_text = clean_tweet_text(text, "normal")

        if cleaned_text == "":
            continue

        tweets[cleaned_text].append(tweet.get("favorite_count", 0))

    summed_likes = {val: floor(mean(int(idx) for idx in key)) for val, key in tweets.items()} # averaging number of likes for duplicate posts

    sorted_likes = sorted(summed_likes.items(), key=lambda x: x[1], reverse=True) # sorting posts by number of likes

    rearranged_dict = {key: val for key, val in sorted_likes} # convert tuple into dictionary

    return rearranged_dict

# saves list of tweets to given output path (text file)
def save_tweets_to_txt(tweets: list[str], output_path:str):
    with open(output_path, "w", encoding="utf-8") as f:
        for tweet in tweets:
            f.write(tweet + "\n")

# saves dictionary of tweets to given output path (json file)
def save_tweets_to_json(tweets: dict, output_path:str):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tweets, f, ensure_ascii=False)

# execute complete tweet cleaning pipeline
def run_pipeline(input_path:str, output_path:str):
    raw_tweets = load_raw_file(input_path)

    #if cleaned tweets files do not exist, process tweets and save them
    if not os.path.exists(output_path):
        tweets = process_tweets_to_list(raw_tweets, "normal")
        save_tweets_to_txt(tweets, output_path)
        print(f"Processed {len(tweets)} tweets")

    output_path_no_replies = output_path[:-4] + "_no_mentions.txt"
    if not os.path.exists(output_path_no_replies):
        tweets = process_tweets_to_list(raw_tweets, "no_replies")
        save_tweets_to_txt(tweets, output_path_no_replies)

    output_path_alt = output_path[:-4] + "_with_likes.json"
    if not os.path.exists(output_path_alt):
        tweets = process_tweets_to_dict(raw_tweets)
        save_tweets_to_json(tweets, output_path_alt)