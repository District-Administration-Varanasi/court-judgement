# Steps to get started:

 1. Create a .env file in the same directory as of main.py.
 2. Paste the following line and replace `{YOUR_CODE}` with your OpenAI API key.
 `OPENAI_API_KEY={YOUR_KEY}`

 3. (Optional) Create a new conda environment and activate it. 
 4. Install all the requirements using requirements.txt file
 5. Now run the main.py file.
 6. After the copilot asks questions in JSON format, you either answer all the questions in JSON format or use the attempt1.json by copy pasting the JSON data.
 7. If the answers are irrelevant then the copilot will again ask reframed questions for only those wrong answers, otherwise it will go to the next step.
 8. When you have answered all the questions the copilot will generate a JSON data with name "commondata.json" and a draft by the name "Draft.txt" using the create.py module.


# Sample Workflow: 



### Document Dict 
For a document - a json of questions are created by LLM which has all the key details in the doc.
  
{"key1":"value1",
"key2":"value2",
"key3":"value3",
"key4":"value4",
"key5":"value5",
"key6":"value6"}



### Document Question dict 

Based on the json dict, questions are asked to the user : 

{"key1":["Q1.1","Q1.2"],
"key2":["Q2"],
"key3":["Q3"],
"key4":["Q4"],
"key5":["Q5"],
"key6":["Q6"]}




### User answer dict : 
The user answers the questions with answers  :
{"Q1.1":"answer1.1",
"Q1.2":"answer1.2",
"Q2":"answer3",
"Q2":"answer4",
"Q2":"answer5",
"Q2":"answer6"}



### User doc dict
the LLM then creates a user specific user dict based  on the answer, it adds values only if the answer is relevant, if irrelevant it leaves it blank

{"key1":"",
"key2":"value2",
"key3":"value3",
"key4":"value4",
"key5":"",
"key6":"value6"}


### Question recreated dict : 

Only for blank keys, questions are recreated based on 

{"key1":["Q1.3"],
"key5":["Q5.1"],
}

## 


