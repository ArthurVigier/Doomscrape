import openai
from dotenv import load_dotenv
import os

load_dotenv(.env)
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_tweet_sentiment (tweet):
  messages = [
    {"role": "system", "content": "you are a sentiment analysis assistant. Given a text in"}
    {"role": "user", "content": "The way Frank Ocean continues to finesse y'all into believ"}
    {"role": "assistant", "content": "negative"}, 
    {"role": "user", "content": tweet}
  ]

  res = openai.ChatCompletion.create (
    model=" gpt-4", 
    messages-messages
 )
return res["choices"][0]["message"]["content"]


"""

Example 

get_tweet_sentiment ("frank ocean performing godspeed. i'm so moved")

'positive'

get_tweet_sentiment ("It could have been better but it wasn't a terrible set either")

'neutral'

"""