import os
import PyPDF2
import yaml
import autogen
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from IPython import get_ipython

# PDF processing function
def process_pdfs(directory):
    """
    Process all PDF files in the specified directory, converting them to text files with the same name.

    Args:
        directory (str): The directory containing PDF files to be processed.
    """
    def convert_pdf_to_text(pdf_path):
        """
        Convert a single PDF file to a text file with the same name.

        Args:
            pdf_path (str): The path to the PDF file to be converted.
        """
        output_txt_path = pdf_path.replace('.pdf', '.txt')
        with open(pdf_path, 'rb') as pdf_file, open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                txt_file.write(text)
        return output_txt_path

    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory, filename)
            convert_pdf_to_text(pdf_path)

# Load configuration
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# Set up OpenAI configuration
OAI_CONFIG_LIST = {
    'model': config['openai']['model'],
    'api_key': config['openai']['api_key']
}

OPENAI_MODEL = config['openai']['model']

config_list = [{
    "model": OPENAI_MODEL,
    "api_key": config['openai']['api_key']
}]

# LLM configuration
llm_config = config['llm_config']
llm_config['config_list'] = config_list

# Project settings
PATH = eval(config['project']['path'])  # Evaluate the string to get the actual path
batch_size = config['project']['batch_size']

# Function definitions
def exec_python(cell):
    ipython = get_ipython()
    result = ipython.run_cell(cell)
    log = str(result.result)
    if result.error_before_exec is not None:
        log += f"\n{result.error_before_exec}"
    if result.error_in_exec is not None:
        log += f"\n{result.error_in_exec}"
    return log

def exec_sh(script):
    return user_interface.execute_code_blocks([("sh", script)])

# Create agents
schema_generator = autogen.AssistantAgent(
    name=config['agents']['schema_generator']['name'],
    llm_config=llm_config,
    system_message=config['agents']['schema_generator']['system_message'].format(
        example_document=config['example_document'],
        example_schema=config['example_schema'],
        batch_size=batch_size
    )
)

user_interface = autogen.UserProxyAgent(
    name=config['agents']['user_interface']['name'],
    system_message=config['agents']['user_interface']['system_message'],
    code_execution_config=config['agents']['user_interface']['code_execution_config'],
    max_consecutive_auto_reply=config['agents']['user_interface']['max_consecutive_auto_reply'],
    llm_config=llm_config,
    human_input_mode=config['agents']['user_interface']['human_input_mode']
)

critique = autogen.AssistantAgent(
    name=config['agents']['critique']['name'],
    llm_config=llm_config,
    system_message=config['agents']['critique']['system_message']
)

# Register functions
schema_generator.register_function(function_map={"python": exec_python})
critique.register_function(function_map={"python": exec_python})

# Set up GroupChat
groupchat = autogen.GroupChat(
    agents=[user_interface, schema_generator, critique], 
    messages=[], 
    max_round=config['groupchat']['max_round']
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Main pipeline
if __name__ == "__main__":
    # Step 1: Process PDFs
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)
    print("Current working directory:", os.getcwd())
    process_pdfs(directory)
    
    # Step 2: Initiate agent chat
    user_interface.initiate_chat(
        manager,
        message=config['initial_message'].format(PATH=PATH)
    )