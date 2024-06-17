import os
import PyPDF2

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

# Example usage:
if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(directory)
    print("Current working directory:", os.getcwd())
    process_pdfs(directory)
