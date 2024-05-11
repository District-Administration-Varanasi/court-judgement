from openai import OpenAI
from dotenv import load_dotenv
import json
import subprocess

load_dotenv()

client = OpenAI()


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def generate_questions():
    json_schema = load_json('commonDetails.json')
    json_schema_str = json.dumps(json_schema)
    schema_example = load_json('detailsExample.json')
    schema_example_str = json.dumps(schema_example)
    questionExample = load_json('questionsExample.json')
    question_str = json.dumps(questionExample)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            
            {"role": "system", "content": '''You are an AI assistant who frames questions in JSON data format for a set JSON schema and uses an example for reference. You only return JSON data containing questions and nothing else. Example:
            JSON Schema: ''' + schema_example_str +
            '''Questions JSON data:''' + question_str
            },
            {"role": "user", "content":'''
            JSON Schema:''' + json_schema_str +
            '''Questions JSON data:''' 
            }
        ]
    )
    return completion.choices[0].message.content

q_generated_str = generate_questions()
print(q_generated_str)


chat_history = []
def generate_response(user_input):
    
    prompt = " ".join(chat_history) + user_input
    json_schema = load_json('commonDetails.json')
    json_schema_str = json.dumps(json_schema)
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''You are an AI assistant that recreates questions whose answers are impertinent or irrelevant and ask those questions in JSON format. Everytime you only ask those questions whose answer needs to be filled or changed. When all answers are relevant and pertinent enough then print only "Done". 
            The questions JSON data is: '''
            + q_generated_str + 
            '''JSON Schema to be filled and returned:''' + json_schema_str},
            {"role": "user", "content": prompt}
        ]
    )

    reply = completion.choices[0].message.content

    if reply == "Done":
        prompt2 = "Just give the filled JSON data"
        prompt2 = " ".join(chat_history) + prompt2
        completion2 = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": '''You are an AI assistant that recreates questions whose answers are impertinent or irrelevant and ask those questions in JSON format. Everytime you only ask those questions whose answer needs to be filled or changed. When all answers are relevant and pertinent enough then return only the filled JSON schema. 
                The questions JSON data is: '''
                + q_generated_str + 
                '''JSON Schema to be filled and returned:''' + json_schema_str},
                {"role": "user", "content": prompt2}
            ]
        )

        filled_json_str = completion2.choices[0].message.content

    else:
        filled_json_str = "All the questions not answered!"
        

    chat_history.append(reply)
    return reply, filled_json_str

filled_json_str=""
response=""

while response!="Done":
    user_input = input("You: ")
    response, filled_json_str = generate_response(user_input)
    print("Chatbot:", response)

filled_json = json.loads(filled_json_str.strip())

with open("usercommon.json", "w") as json_file:
    json.dump(filled_json, json_file)

subprocess.run(['python','create.py'])
