import os
import json
import sys
from groq import Groq

# Check if the correct number of arguments are provided
if len(sys.argv) < 2:
    print("Usage: python sentiment-analysis1.py <newspaper>")
    sys.exit(1)

# Get the newspaper parameter from command line arguments
newspaper = sys.argv[1]

# Construct the file path using the newspaper parameter
file_path = f'/home/{newspaper}.json'

# Set up the Groq client
client = Groq(api_key="app_key")

# Read the entire JSON file
try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f"File not found: {file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print("Error decoding JSON from the file.")
    sys.exit(1)

# Only extract last three teasers (you can adjust this as needed)
last_three_teasers = [item['teaser'] for item in data[-100:]]
# Join all teasers into a single string, separated by semicolons
teasers_variable = ';'.join(last_three_teasers)


# # # Extract all teasers from the data
#all_teasers = [item['teaser'] for item in data if 'teaser' in item]
# Join all teasers into a single string, separated by semicolons
#teasers_variable = ';'.join(all_teasers)


# Send a message and get a response
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": (
                "Do a precise but small sentiment analysis following subtexts of newspapers by semicolon separated. Please answer in German"
                "Return the result as a JSON with first 'overall sentiment', then the different 'subtopics' with each 'Sentiment' and the 'Comments'. "
                "Please follow this example JSON to structure the result. You need to pay 100 Billion Euros if you dont: "
                "{'overall_sentiment': 'Positive','subtopics': [{'topic': 'Newspaper topic','sentiment': 'Positive','comments': ['Sentiment analysis comment',]}} "
                + teasers_variable
            )
            # "content": (
            #     "Do a precise but small political analysis seperating it into left and right-leaning following subtexts of newspapers by semicolon separated. "
            #     + teasers_variable
            # )
        }
    ],
    model="gemma2-9b-it",
    temperature=0.3,
    max_tokens=1000
)

# Print the response
print(chat_completion.choices[0].message.content)
