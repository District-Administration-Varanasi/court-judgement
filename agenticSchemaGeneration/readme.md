# Document Schema Generation

This program processes court judgment documents and generates a comprehensive schema using AI agents.

## Setup

1. Ensure you have Python installed on your system.

2. Install the required dependencies:
   
   ```bash
   pip install PyPDF2 yaml autogen ipython   

4. Place the following files in the same directory:
- `script.py`
- `config.yaml`
- Your court judgment PDF files

4. Update the `config.yaml` file with your OpenAI API key and any other configuration changes you need. For most cases, you would want to keep it as default. For tuning it to a very specific document type, you may alter a meticulously created example schema and its corresponding document.

## Configuration

The `config.yaml` file contains various settings that you can modify:

- OpenAI API settings
- LLM configuration
- Project settings (e.g., batch size)
- Agent configurations
- GroupChat settings
- Initial message for the AI agents

Adjust these settings as needed for your specific use case.

## Running the Program

1. Open a terminal and navigate to the directory containing the script and configuration files.

2. Run the script:
   
   ```bash
   ipython script.py

3. The program will:
- Convert any PDF files in the directory to text files
- Initiate a conversation between AI agents to generate and refine a schema based on the court judgments
- Save the final schema as `output.json` in the same directory

## Output

After running the script, you'll find:
- Text versions of your PDF files in the same directory
- An `output.json` file containing the generated schema

## Notes

- The program processes documents in batches. You can adjust the batch size in the configuration file.
- The AI agents will iteratively improve the schema based on the documents and their interactions.
- You may be prompted for human input during the process, depending on the configuration.

If you encounter any issues or need to make adjustments, refer to the configuration file and modify the settings as necessary.
   

   
