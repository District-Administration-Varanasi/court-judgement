from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

chat_history = []

def load_json_schema(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_response(user_input):
    # Craft the request to OpenAI API including chat history
    prompt = " ".join(chat_history) + user_input
    json_schema = load_json_schema('commonDetails.json')
    json_schema_str = json.dumps(json_schema)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f'You are given the following json schema to be filled. You have to ask me questions such that i will give you have sufficient information to fill in the given json schema. If some answers are missing then again frame some questions for the left out ones. Keep asking for unanswered ones upto 3 times and after that return the filled json schema. The JSON Schema is: {json_schema_str}'},
            {"role": "user", "content": prompt}
        ]
    )
    chat_history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

while True:
    user_input = input("You: ")
    response = generate_response(user_input)
    print("Chatbot:", response)
