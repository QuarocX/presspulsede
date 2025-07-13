import os
import json
from groq import Groq

# Set up the Groq client
client = Groq(api_key="api_KEY")

# open Json File
with open('/home/sueddeutsche.json', 'r') as file:
    data = json.load(file)

last_three_teasers = [item['teaser'] for item in data[-3:]]
teasers_variable = ';'.join(last_three_teasers)

print(teasers_variable)
print('')


# Send a message and get a response
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Do a precise but small sentiment analysis following subtexts of newspapers by semikolon separated: " + teasers_variable
        }
    ],
    model="gemma-7b-it",
    temperature=0.7,
    max_tokens=1000
)

# Print the response
print(chat_completion.choices[0].message.content)
