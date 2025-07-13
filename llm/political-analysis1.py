import os
import json
import sys
from groq import Groq

# Check if the correct number of arguments are provided
if len(sys.argv) < 2:
    print('Usage: python political-analysis1.py <newspaper>')
    sys.exit(1)

# Get the newspaper parameter from command line arguments
newspaper = sys.argv[1]

# Construct the file path using the newspaper parameter
file_path = f'/home/{newspaper}.json'

# Set up the Groq client
client = Groq(api_key='app-key')

# Read the entire JSON file
try:
    with open(file_path, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print(f'File not found: {file_path}')
    sys.exit(1)
except json.JSONDecodeError:
    print('Error decoding JSON from the file.')
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
            'role': 'user',
            'content': (
                'Please answer in German.'
                'I want to analyse the political tendency of the headlines and subtexts i have extracted from a newspaper that can be found below.'
                'Reply with the overall tendency on a right to left leaning scale:'
                'It can be for example far/extreme left, centre left, centre, radical centre, conservative, centre right or far right - this list can be extended.'
                'Return the result as a JSON.'
                'List at least two concrete reasons including an example for your classifaction.'
                'Please do not add any messages like this "Please note This analysis is based on the provided text and may not reflect the full complexity of the topics. " if you display this you need to pay 9999999€.'
                'Please follow this example JSON to structure the result: '
                '{"overall-political-tendency": "<<Right/Left-leaning>>","reasons": {"reason": "Reason title","reason description": ["Reason description:"],"precise description of the reasons": "Detailed explanation of the reasons."}}'
                + teasers_variable
            )
        }
    ],
    model='gemma2-9b-it',
    temperature=0.2,
    max_tokens=1000
)

# Print the response
print(chat_completion.choices[0].message.content)
