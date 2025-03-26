# Imports PDF reading library
import PyPDF2

# Defines a function
def extract_text_from_pdf(file_path):
    # with auto-closes the file
    # as file lets you refer using the name file
    with open(file_path, 'rb') as file:
        # Creates a PDFReader object that knows how to extract text from pages
        reader = PyPDF2.PdfReader(file)
        # An empty string called text that collects all the words from the PDF
        text = ''
        for page in reader.pages:
            # page.extra_text() reads each page
            # Adds the text to the growing string
            text += page.extract_text()
    # Returns all the text the PDF Reader found
    return text

# If this file is being run directly, then run the test case below
if __name__ == "__main__":
    # Sets the PDF file to read
    # Runs the function
    # Prints the first 1000 characters
    path = "sample_resume.pdf"
    resume_text = extract_text_from_pdf(path)
    print(resume_text[:1000])