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
            {"role": "system", "content": '''You are an AI assistant who frames questions in JSON style for 'all the keys' of given set JSON schema and who uses an example for reference. You only return JSON data containing questions and nothing else. Example:
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
            {"role": "system", "content": '''You are an AI assistant that creates new questions in JSON format which should be different than "Earlier questions". Questions should be asked for some  "Expected answers" so frame the new questions accordingly. Make sure not to recreate the "Earlier questions".'''
            },
            {"role": "user", "content":
            '''Earlier questions:''' + Q_dict_earlier +
            '''Expected answers:''' + expected_dict_ans 
            }
        ]
    )
    return completion.choices[0].message.content

def convert_ans(ans_str):
    translated = load_json('engTranslateExample.json')  
    translated_str = json.dumps(translated) 
    original = load_json('hinTranslateExample.json')  
    original_str = json.dumps(original) 
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #Prompt hindi to eng ans.
            {"role": "system", "content": '''You are an AI assistant that translates the values of JSON properties into English. 'Original values' JSON will be given and you have to create 'Translated values' JSON. Example:
             Original values: ''' + original_str +
             '''Translated values:''' + translated_str
            },
            {"role": "user", "content":
            '''Original values: ''' + ans_str +
            '''Translated values: '''
            }
        ]
    )
    return completion.choices[0].message.content

def convert_q(q_str):
    translatedQ = load_json('hinQExample.json') 
    translatedQ_str = json.dumps(translatedQ) 
    originalQ = load_json('questionsExample.json') 
    originalQ_str = json.dumps(originalQ) 
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #Prompt eng to hindi Q.
            {"role": "system", "content": '''You are an AI assistant that translates the JSON values of question properties into Hindi. 'Original questions' JSON will be given and you have to create 'Translated questions' JSON. Example:
             Original questions: ''' + originalQ_str +
             '''Translated questions:''' + translatedQ_str
            },
            {"role": "user", "content":
            '''Original questions: ''' + q_str +
            '''Translated questions: '''
            }
        ]
    )
    return completion.choices[0].message.content


################################################# BEGINS ###################################################

q_1_str = generate_questions()
hin_q_str = convert_q(q_1_str)
print(hin_q_str)
q_dict = json.loads(q_1_str)
print("\n आपके उत्तर JSON प्रारूप में: \n")
user_ans_str_hin = input("")

json_schema_dict = load_json('commonDetails.json') #common details JSON schema dictionary
json_example_dict = load_json('exampleSchema-2.json') #Example of filled JSON data with expected values

while True:

    user_ans_str = convert_ans(user_ans_str_hin)
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
        q_dict = json.loads(Q_dict_2_str) #to reuse
        hin_Q_dict_2_str = convert_q(Q_dict_2_str)
        print(hin_Q_dict_2_str)

        #User gives new answers
        print("\n आपके उत्तर JSON प्रारूप में: \n")
        user_ans_str_hin=input("")
    
    else:
         break

with open("usercommon.json", "w") as json_file:
    json.dump(filled_dict, json_file)

import create

draft = create.generate_response()

with open("Draft.txt", "w") as text_file:
    text_file.write(draft)
