from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

chat_history = []

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def generate_response(user_input):
    
    prompt = " ".join(chat_history) + user_input
    json_schema = load_json('details.schema.json')
    json_schema_str = json.dumps(json_schema)
    questionExample = load_json('questionsExample.json')
    question_str = json.dumps(questionExample)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f'You are given a json schema to be filled. The JSON schema is {json_schema_str}. You have to ask me questions in similar JSON style like {question_str} such that i will give you sufficient information for all key-value pairs of json schema to be filled. If i answer something invalid or irrelevant or impertinent then reframe those questions and ask only those questions next time.'},
            {"role": "user", "content": prompt}
        ]
    )
    chat_history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

while True:
    user_input = input("You: ")
    response = generate_response(user_input)
    print("Chatbot:", response)
