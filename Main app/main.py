from openai import OpenAI
from dotenv import load_dotenv
import json
import requests
import time
import os
load_dotenv()

class AzureAdapter():
    def _init_(self):
        self.subscription_key = os.environ.get("AZURE_SUBSCRIPTION_KEY")

    def translate_text(self, text,source_language, target_language):

        url = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}".format(source_language, target_language)
        headers = {
            "Ocp-Apim-Subscription-Key": "38a3485f022e47fc845aca60612967eb",
            'Ocp-Apim-Subscription-Region': "southeastasia",
            "Content-Type": "application/json; charset=UTF-8"
        }
        payload = [{"Text": text}]

        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload)
        end_time = time.time()
        latency=end_time-start_time

        response.raise_for_status()

        translated_text = response.json()[0]['translations'][0]['text']

        return translated_text, latency


client = OpenAI()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def generate_questions():
    json_example = load_json('schemaNexamples.json') #Example of filled JSON data with expected values
    json_example_str = json.dumps(json_example)
    small_example = load_json('detailsExample2.json') #Small example of filled JSON data
    small_example_str = json.dumps(small_example)
    questionExample = load_json('questionsExample2.json') #Small example of questions
    question_str = json.dumps(questionExample)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #Prompt 1
            {"role": "system", "content": '''You are an AI assistant who frames questions in JSON style for "all the keys" of given 'JSON Schema' and returns 'Questions JSON'. You only return JSON data containing questions and nothing else. Example:
            JSON Schema: ''' + small_example_str +
            '''Questions JSON:''' + question_str
            },
            {"role": "user", "content":'''
            JSON Schema:''' + json_example_str +
            '''Questions JSON:''' 
            }
        ]
    )
    return completion.choices[0].message.content

def fill_JSON_schema(user_ans_str, already_filled_str):

    current = load_json('currentExample.json') #common details JSON schema 
    current_str = json.dumps(current) 
    input = load_json('inputExample.json') #common details JSON schema 
    input_str = json.dumps(input) 
    expected = load_json('expectedExample.json') #common details JSON schema 
    expected_str = json.dumps(expected) 
    newCurrent = load_json('newCurrentExample.json') #common details JSON schema 
    newCurrent_str = json.dumps(newCurrent)
    json_example = load_json('schemaNexamples.json') #Example of filled JSON data with expected values
    json_example_str = json.dumps(json_example)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            #Prompt 2
            {"role": "system", "content": '''You are an AI assistant that fills values from "User input" in the "Current JSON" and return "New JSON". Remember if the value in "User input" is irrelevant or invalid, then store null in that same property of "Current JSON" or leave it empty if it stores a list. The examples in "JSON Schema" must be used as a 'reference to judge' the values in "User input", for if they are valid enough to fill in "Current JSON". Return New JSON string without new lines or code fence. Example: 
               Current JSON:''' + current_str +  
            '''User input:''' + input_str +
            '''JSON Schema:''' + expected_str +
            '''New JSON:''' + newCurrent_str
            },
            {"role": "user", "content":
            '''Current JSON:''' + already_filled_str +
            '''User input:''' + user_ans_str +
            '''JSON Schema:''' + json_example_str +
            '''New JSON:'''
            }
        ]
    )
    return completion.choices[0].message.content

def reframe_Q(Q_dict_earlier, expected_dict_ans):
    #print(Q_dict_earlier + "\n")
    #print(expected_dict_ans + "\n")
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            #Prompt 3
            {"role": "system", "content": '''You are an AI assistant that creates new questions, that mean the same as in "Earlier questions" JSON. Questions should be asked for examples given in "Expected answers" so frame the new questions accordingly. Make sure to keep the same keys as in "Earlier questions" JSON but store new questions for each key. Return just JSON string without new lines or code fence or anything else.'''
            },
            {"role": "user", "content":
            '''Earlier questions:''' + Q_dict_earlier +
            '''Expected answers:''' + expected_dict_ans 
            }
        ]
    )
    #print(completion.choices[0].message.content + "\n")
    return completion.choices[0].message.content

def convert_q(q_str):
    eng_q = json.loads(q_str)
    azure = AzureAdapter()
    
    def translate_dict(d):
        for key, value in d.items():
            if isinstance(value, str):
                temp = azure.translate_text(value, "en-US", "hi-IN")
                d[key] = temp[0]
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], str):
                        temp = azure.translate_text(value[i], "en-US", "hi-IN")
                        value[i] = temp[0]
        return d

    translated_q = translate_dict(eng_q)
    translated_q_str = json.dumps(translated_q)
    return translated_q_str

def print_q(q_str):
    q = json.loads(q_str)
    for key, value in q.items():
        if isinstance(value, str):
            print(key, ":", value, "\n")
        elif isinstance(value, list):
            print(key, ":")
            for i in range(len(value)):
                print(value[i], ", ")
            print("\n")

def print_ans(ans_str):
    ans = json.loads(ans_str)
    for key, value in ans.items():
        if isinstance(value, str):
            print(key, ":", value, "\n")
        elif isinstance(value, list):
            print(key, ":")
            for i in range(len(value)):
                print(value[i], ", ")
            print("\n")

def convert_ans(ans_str):
    hin_ans = json.loads(ans_str)
    azure = AzureAdapter()
    
    def translate_dict(d):
        for key, value in d.items():
            if isinstance(value, str):
                #print(value)
                temp = azure.translate_text(value, "hi-IN", "en-US")
                d[key] = temp[0]
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], str):
                        temp = azure.translate_text(value[i], "hi-IN", "en-US")
                        value[i] = temp[0]
        return d

    translated_ans = translate_dict(hin_ans)
    translated_ans_str = json.dumps(translated_ans)
    return translated_ans_str
    
def check_dict(d, q_dict, expected):
    unans_q = {}
    unans_expected_v = {}
    for key, value in d.items():
        if value is None or value == []:
            #print(key)
            unans_q[key] = q_dict[key]
            unans_expected_v[key] = expected[key]
    return unans_q, unans_expected_v

def create_null_json(input_json_path, output_json_path):
    # Load the input JSON file
    with open(input_json_path, 'r') as input_file:
        data = json.load(input_file)

    # Create a new dictionary with null values or empty lists based on the input schema
    null_data = {}
    for key, value in data.items():
        if value['type'] == 'array':
            null_data[key] = []
        else:
            null_data[key] = None

    # Write the new dictionary to the output JSON file
    with open(output_json_path, 'w') as output_file:
        json.dump(null_data, output_file, indent=2)


################################# BEGINS ###################################################

#INITIALIZATION:    

#creating questions
q_1_str = generate_questions()
q_dict = json.loads(q_1_str)

#print hindi questions
hin_q_str = convert_q(q_1_str)
print_q(hin_q_str)

#storing user answers
print("\n आपके उत्तर JSON प्रारूप में: \n")
user_ans_str_hin = input("")

#creating expected JSON values   
expected_dict_ans = load_json('schemaNexamples.json') 
#expected_ans_str = json.dumps(expected_dict_ans)

#creating empty or null JSON object
input_json_path = 'schemaNexamples.json'
output_json_path = 'emptyDetails.json'
create_null_json(input_json_path, output_json_path)
current_json = load_json('emptyDetails.json') 
current_json_str = json.dumps(current_json)


#loop for filling current JSON object and reframing questions:
while True:

    #convert user ans to english
    user_ans_str = convert_ans(user_ans_str_hin)
    #print(user_ans_str)
    #fill current JSON
    current_json_str = fill_JSON_schema(user_ans_str, current_json_str)
    #print(current_json_str)
    current_json = json.loads(current_json_str)
    #print("filling of current json done")

    #iterate over current JSON to get unanswered questions
       
    #Q_dict_unans = {} Dictionary of only those Q that were marked unanswered
    #expected_dict_ans= {} Dictionary of expected answers of above questions

    Q_dict_unans, expected_dict_ans = check_dict(current_json, q_dict, expected_dict_ans)

    #print("\n ---- \n", expected_dict_ans, "\n ---- \n")
    #If all questions are answered:
    if not Q_dict_unans:
        break

    #Question reframing for unanswered questions:

    Q_dict_unans_str = json.dumps(Q_dict_unans)    
    expected_dict_ans_str = json.dumps(expected_dict_ans)    
    new_Q_dict_str = reframe_Q(Q_dict_unans_str, expected_dict_ans_str)

    #store new questions in q_dict:
    q_dict = json.loads(new_Q_dict_str) 

    #convert reframed questions to hindi:
    hin_Q_dict_str = convert_q(new_Q_dict_str)
    print_q(hin_Q_dict_str)

    #User gives new answers
    print("\n आपके उत्तर JSON प्रारूप में: \n")
    user_ans_str_hin=input("")

with open("filledJSON.json", "w") as json_file:
    json.dump(current_json, json_file)

import create

draft = create.generate_response()

with open("Draft.txt", "w") as text_file:
    text_file.write(draft)

print("Draft created successfully!","\n", "Checkout Draft.txt file for the same.")