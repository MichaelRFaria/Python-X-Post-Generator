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
    Instructions:
    You are a social media copywriter who writes high-quality Twitter/X posts that match a specific writing style.
    
    Task:
    Generate 5 original Twitter posts based on the example tweets (posts and/or replies) provided below.
    
    Style reference:
    The examples represent the tone, structure, humor, vocabulary and pacing I want you to imitate. Do not copy them directly. Extract the style and generate your own.
    
    Rules:
    1. Each tweet must be original (no copying or paraphrasing sentences directly)
    2. Keep each tweet under 280 characters
    3. Match the tone, flow and formatting style of the examples
    4. Preserve any common patterns (e.g. humor, threads, hooks, brevity, emojis, etc.)
    5. Avoid repetition across the 5 outputs
    
    Output format:
    Return exactly 5 tweets numbered 1 to 5 with just the post. No extra commentary.
    
    Example tweets:
    {"\n\t".join(tweets)}
    
    """

def generate_posts(input_path: str):
    tweets = get_tweets(input_path)
    random_tweets = get_random_tweets(tweets, 10)
    prompt = create_prompt(random_tweets)

    stream = chat(
        model='tinyllama', # this model sucks ass, but it shows that the code works todo try mistral (4.4gb)
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )

    print("Generating posts...")

    for chunk in stream:
        print(chunk['message']['content'], end='', flush=True)