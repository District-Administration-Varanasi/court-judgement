from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def generate_questions():
    json_example = load_json('exampleSchema-2.json') #Example of filled JSON data with expected values
    json_example_str = json.dumps(json_example)
    small_example = load_json('detailsExample.json') #Small example of filled JSON data
    small_example_str = json.dumps(small_example)
    questionExample = load_json('questionsExample.json') #Small example of questions
    question_str = json.dumps(questionExample)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #Prompt 1
            {"role": "system", "content": '''You are an AI assistant who frames questions in JSON data format for a set JSON schema and uses an example for reference. You only return JSON data containing questions and nothing else. Example:
            JSON Schema: ''' + small_example_str +
            '''Questions JSON data:''' + question_str
            },
            {"role": "user", "content":'''
            JSON Schema:''' + json_example_str +
            '''Questions JSON data:''' 
            }
        ]
    )
    return completion.choices[0].message.content

def fill_JSON_schema(user_ans_1_str):
    json_schema = load_json('commonDetails.json') #common details JSON schema 
    json_schema_str = json.dumps(json_schema) 
    json_example = load_json('exampleSchema-2.json') #Example of filled JSON data with expected values
    json_example_str = json.dumps(json_example)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #Prompt 2
            {"role": "system", "content": '''You are an AI assistant that fills values based on "User input" in the set "JSON Schema" and return it. Remember if the value is irrelevant or impertinent don't fill it and keep that key blank. An "Example" of filled JSON schema must be used as a reference to check if the input data is pertinent enough to fill or keep it blank.'''
            },
            {"role": "user", "content":
            '''JSON Schema:''' + json_schema_str +
            '''User input:''' + user_ans_1_str +
            '''Example:''' + json_example_str
            }
        ]
    )
    return completion.choices[0].message.content

def reframe_Q(Q_dict_earlier, expected_dict_ans):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #Prompt 3
            {"role": "system", "content": '''You are an AI assistant that creates new questions in JSON format which should be different than "Earlier questions". Questions should be asked for some  "Expected answers" so frame the new questions accordingly. Make sure not to recreate the "Earlier questions."'''
            },
            {"role": "user", "content":
            '''Earlier questions:''' + Q_dict_earlier +
            '''Expected answers:''' + expected_dict_ans 
            }
        ]
    )
    return completion.choices[0].message.content

################################################# BEGINS ###################################################

q_1_str = generate_questions()
print(q_1_str)
q_dict = json.loads(q_1_str)
print("\n Your answers in JSON format: \n")
user_ans_str = input("")

json_schema_dict = load_json('commonDetails.json') #common details JSON schema dictionary
json_example_dict = load_json('exampleSchema-2.json') #Example of filled JSON data with expected values

while True:
     
    filled_json_dict_str = fill_JSON_schema(user_ans_str)
    filled_dict = json.loads(filled_json_dict_str)
    print("filling done")

    if any(value is None for value in filled_dict):
        
        Q_unans_dict_earlier = {} #Dictionary of only those Q that were marked unanswered
        json_dict_unans={} #Dictionary of only those json schema that were marked unanswered
        expected_dict_ans={} #Dictionary of expected answers corresponding to those marked unanswered
        for key, value in filled_dict.items():
            if value is None and key in q_dict:
                Q_unans_dict_earlier[key] = q_dict[key]
            if value is None and key in json_schema_dict:
                json_dict_unans[key] = json_schema_dict[key]
            if value is None and key in json_example_dict:
                expected_dict_ans[key] = json_example_dict[key]

        #New Questions asked
        Q_earlier_str = json.dumps(Q_unans_dict_earlier)    
        expected_ans_str = json.dumps(expected_dict_ans)    
        Q_dict_2_str = reframe_Q(Q_earlier_str, expected_ans_str)
        Q_dict_2 = json.loads(Q_dict_2_str)
        print(Q_dict_2_str)

        #User gives new answers
        print("\n Your answers in JSON format: \n")
        user_ans_str=input("")
    
    else:
         break

with open("usercommon.json", "w") as json_file:
    json.dump(filled_dict, json_file)

import create

draft = create.generate_response()

with open("Draft.txt", "w") as text_file:
    text_file.write(draft)
