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