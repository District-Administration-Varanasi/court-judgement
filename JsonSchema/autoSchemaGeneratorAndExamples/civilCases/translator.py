import os
from googletrans import Translator

def translate_text_to_english(text):
    """
    Translate the given text to English.

    Args:
        text (str): The text to be translated.

    Returns:
        str: The translated text in English.
    """
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text

def process_text_files(directory):
    """
    Read all text files in the specified directory, translate their content to English,
    and replace the current content with the translated text.

    Args:
        directory (str): The directory containing text files to be processed.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            txt_path = os.path.join(directory, filename)
            with open(txt_path, 'r', encoding='utf-8') as file:
                original_text = file.read()
            
            translated_text = translate_text_to_english(original_text)
            
            with open(txt_path, 'w', encoding='utf-8') as file:
                file.write(translated_text)

# Example usage:
if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)
    print("Current working directory:", os.getcwd())
    process_text_files(directory)
