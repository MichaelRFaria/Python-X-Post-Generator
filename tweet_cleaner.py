import json
import re

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
def clean_tweet_text(text: str) -> str:
    text = re.sub(r"https://t\.co/\S+", "", text)

    # remove newlines, normalise whitespaces, remove leading and trailing linespaces
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    text.strip()

    #print(text)
    #print(repr(text))

    # if the remaining tweet is just a mention(s), then skip it
    if re.match(r"^(@\w+\s*)+$", text):
        return ""

    # skip empty tweets
    if text == "" or text == " ":  # todo - previous strip should mean that text == " " isn't needed, but for some reason it is necessary
        return ""

    return text

# preprocesses all given tweets
def process_tweets(raw: str) -> list[str]:
    tweets_data = extract_tweets_json(raw)

    tweets = []

    for item in tweets_data:
        tweet = item["tweet"]

        text = tweet.get("full_text", "")

        cleaned_text = clean_tweet_text(text)

        if cleaned_text == "":
            continue

        tweets.append(cleaned_text)

    return tweets

# saves list of tweets to given output path
def save_tweets(tweets: list[str], output_path:str):
    with open(output_path, "w", encoding="utf-8") as f:
        for tweet in tweets:
            f.write(tweet + "\n")


# execute complete tweet cleaning pipeline
def run_pipeline(input_path:str, output_path:str):
    raw_tweets = load_raw_file(input_path)
    tweets = process_tweets(raw_tweets)
    save_tweets(tweets, output_path)
    print(f"Processed {len(tweets)} tweets")