from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import time
import requests

load_dotenv()

client = OpenAI()

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
def load_txt(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
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


def generate_response():
    
    common_data1 = load_json('fullyFilledExample.json')
    common_data_str1 = json.dumps(common_data1)
    common_data2 = load_json('fullyFilledExample2.json')
    common_data_str2 = json.dumps(common_data2)
    # unique_data = load_json('frozenDetails2.json')
    # unique_data_str = json.dumps(unique_data)
    exampleDoc1 = load_txt('example.txt')
    exampleDoc2 = load_txt('example2.txt')

    common_data_user = load_json('filledJSON.json')
    common_data_str_user = json.dumps(common_data_user)
    # unique_data_user = load_json('frozenDetails2.json')
    # unique_data_str_user = json.dumps(unique_data_user)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": '''You are an AI assistant who creates documents using input JSON schema. You only return the document in form of string and nothing else. 
            Example 1: 
            Input JSON schema: '''+common_data_str1+
            #'''Input JSON schema 2:'''+unique_data_str+
            '''Output Document: '''+exampleDoc1+
            '''Example 2:
            Input JSON schema: '''+common_data_str2+
            '''Output Document: '''+exampleDoc2
            },
            {"role": "user", "content": '''
            Input JSON schema:'''+ common_data_str_user+
            #'''Input JSON schema 2:'''+ unique_data_str_user+
            '''Output Document:'''}
        ]
    )

    return completion.choices[0].message.content

response = generate_response()

azure = AzureAdapter()

draft = azure.translate_text(response, "en-US", "hi-IN")

with open("Draft.txt", "w") as text_file:
    text_file.write(response)

with open("DraftTranslated.txt", "w") as text_file:
    text_file.write(draft[0])
