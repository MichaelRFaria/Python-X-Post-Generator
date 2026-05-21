import random
from ollama import chat

# gets cleaned tweets from given input path
def get_tweets(input_path:str) -> list[str]:
    tweets = []

    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            tweets.append(line.strip())

    return tweets

# gets random tweets given the tweets and amount to sample
def get_random_tweets(tweets: list[str], num: int) -> list[str]:
    return random.sample(tweets, num)

def create_prompt(tweets: list[str]) -> str:
    return f"""
    Below are tweets from a user.
    
    Write 5 NEW tweets that could realistically come from the same account.
    
    Rules:
    - Be concise
    - Do not explain the jokes
    - No hashtags
    - No moralising
    - No "as an AI"
    - Avoid sounding inspirational or corporate
    - Match the bizzare/confident/internet-poisoned tone of the examples
    - Tweets should feel casually unhinged, not tryhard random
    - Keep tweets short unless longer structure feels natural
    - Do not copy lines directly
    
    Examples:
    {"\n\t".join(tweets)}
    
    
    Output only the tweets.
    """

def generate_posts(input_path: str):
    tweets = get_tweets(input_path)
    random_tweets = get_random_tweets(tweets, 10)
    prompt = create_prompt(random_tweets)

    stream = chat(
        model='llama3.1:8b',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    print(prompt)

    print("Generating posts...")

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)