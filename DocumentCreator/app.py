from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

chat_history = []

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def load_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()


def generate_response(user_input):
    
    prompt = " ".join(chat_history) + user_input
    common_data = load_json('commonData.json')
    common_data_str = json.dumps(common_data)
    unique_data = load_json('uniqueData.json')
    unique_data_str = json.dumps(unique_data)
    exampleDoc = load_txt('example.txt')

    common_data_user = load_json('usercommon.json')
    common_data_str_user = json.dumps(common_data_user)
    unique_data_user = load_json('userunique.json')
    unique_data_str_user = json.dumps(unique_data_user)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''You are an AI assistant who creates documents using 2 input JSON schemas. You only return the document in form of string and nothing else. For example: 
            Input JSON schema 1: '''+common_data_str+
            '''Input JSON schema 2:'''+unique_data_str+
            '''Output Document: '''+exampleDoc
            },
            {"role": "user", "content": '''
            Input JSON schema 1:'''+ common_data_str_user+
            '''Input JSON schema 2:'''+ unique_data_str_user+
            '''Output Document:'''}
        ]
    )
    chat_history.append(completion.choices[0].message.content)
    return completion.choices[0].message.content

while True:
    user_input = input("You: ")
    response = generate_response(user_input)
    print("Chatbot:", response)
