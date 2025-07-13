import os
import json
from groq import Groq

# Set up the Groq client
client = Groq(api_key="app_key")


# Read the entire JSON file
with open('/home/sueddeutsche.json', 'r') as file:
    data = json.load(file)

#only extract last three -> when testing
last_three_teasers = [item['teaser'] for item in data[-10:]]
# Join all teasers into a single string, separated by semicolons
teasers_variable = ';'.join(last_three_teasers)

# # # Extract all teasers from the data
# all_teasers = [item['teaser'] for item in data if 'teaser' in item]
# # Join all teasers into a single string, separated by semicolons
# teasers_variable = ';'.join(all_teasers)

# Print the result
#print('input loaded')
#print('start sending to llm')


# Send a message and get a response
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Do a precise but small sentiment analysis following subtexts of newspapers by semikolon separated. Return the result as a json with first 'overall sentiment', then the different 'subtopics' with each 'Sentiment' and the 'Comments'"
            + "Please follow this example json to structure the result: "
            + "{'overall_sentiment': 'Positive','subtopics': [{'topic': 'Newspaper topic','sentiment': 'Positive','comments': ['Sentiment analysis comment',]}}"
            + teasers_variable
        }
    ],
    model="gemma-7b-it",
    temperature=0.7,
    max_tokens=1000
)

# Print the response
print(chat_completion.choices[0].message.content)
