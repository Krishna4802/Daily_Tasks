 Python code for Resume data extraction


import fitz

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    
    text = ""
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    
    pdf_document.close()
    
    return text

pdf_path = "/Users/krishnaprasath/Downloads/official-ms-word-resume-template.pdf"  
text = extract_text_from_pdf(pdf_path)
print(text)




import fitz
import google.generativeai as genai
import os

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)

    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()

    pdf_document.close()
    # print(text)
    return text

pdf_path = "/Users/krishnaprasath/Downloads/official-ms-word-resume-template.pdf"
text = extract_text_from_pdf(pdf_path)
contect = text + """Given a following resume text, extract the following entities and organize them as dictinory with keys: Name, Email, Mobile number, Experience in years (Mark Zero if a fresher), Top 5 technical skills mentioned, College name, Year of passout, Degree, Branch, Known language, current location and probability of moving to Coimbatore. make sure has following keys: Name, Email, Mobile number, Experience in years, Top 5 technical skills, College name, Year of passout, Degree, Branch, Known language, current location, and add similarity scores each as new fields for Data Engineering/SQL/ETL, Web Development/Full Stack Development, Testing, Dev Ops and resume strength based on industry level of a fresher"""
#print(content)
genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content(contect)
# print(response.text)




import os
import fitz
import google.generativeai as genai

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()
    return text

def process_resume_data(response_text):

    start_idx = response_text.find("{")
    end_idx = response_text.rfind("}")

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Invalid response format: Missing start or end of dictionary assignment.")


    resume_data_str = response_text[start_idx:end_idx + 1]


    try:
        resume_data = eval(resume_data_str)
        return resume_data
    except Exception as e:
        raise ValueError(f"Error evaluating resume_data string: {str(e)}")

def find_key(resume_data, search_terms):
    """
    Find a key in the resume_data dictionary that matches any of the search_terms.
    """
    for key in resume_data.keys():
        if any(term.lower() in key.lower() for term in search_terms):
            return resume_data[key]
    return "Not available"

pdf_path = "/Users/krishnaprasath/Downloads/standout-ms-word-resume-template.pdf"
# pdf_path = "/Users/krishnaprasath/Downloads/official-ms-word-resume-template.pdf"

resume_text = extract_text_from_pdf(pdf_path)

context = resume_text + """
Given the following resume text, extract the following entities and organize them as a dictionary with keys: Name, Email, Mobile number, Experience in years (Mark Zero if a fresher), Top 5 technical skills mentioned, College name, Year of passout, Degree, Branch, Known language, current location and probability of moving to Coimbatore. Make sure it has the following keys: Name, Email, Mobile number, Experience in years, Top 5 technical skills, College name, Year of passout, Degree, Branch, Known language, current location, and add similarity scores each as new fields for Data Engineering/SQL/ETL, Web Development/Full Stack Development, Testing, Dev Ops, and resume strength based on industry level of a fresher."""

genai.configure(api_key=os.environ["API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content(context)

# print(response.text)

try:
    resume_data = process_resume_data(response.text)
    # print(resume_data)

    print("Name:", find_key(resume_data, ["Name"]))
    print("Email:", find_key(resume_data, ["Email"]))
    print("Mobile number:", find_key(resume_data, ["Mobile number"]))
    print("Experience in years:", find_key(resume_data, ["Experience in years"]))
    print("Probability of moving to Coimbatore:", find_key(resume_data, ["Probability of moving to Coimbatore"]))
    print("Top 5 technical skills:", find_key(resume_data, ["Top 5 technical skills"]))
    print("Similarity Scores:")
    print("- Data Engineering/SQL/ETL:", find_key(resume_data, ["Data Engineering/SQL/ETL"]))
    print("- Web Development/Full Stack Development:", find_key(resume_data, ["Web Development/Full Stack Development"]))
    print("- Testing:", find_key(resume_data, ["Testing"]))
    print("- Dev Ops:", find_key(resume_data, ["Dev Ops"]))
    print("Resume strength:", find_key(resume_data, ["Resume Strength", "resume strength", "Strength"]))
    
except Exception as e:
    print(f"Error processing resume data: {str(e)}")



—————————————————————————————————————————————————————————————————————————————


import os
import fitz
import google.generativeai as genai

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    pdf_document.close()
    return text

def process_resume_data(response_text):
    start_idx = response_text.find("{")
    end_idx = response_text.rfind("}")

    if start_idx == -1 or end_idx == -1:
        raise ValueError("Invalid response format: Missing start or end of dictionary assignment.")

    resume_data_str = response_text[start_idx:end_idx + 1]

    try:
        resume_data = eval(resume_data_str)
        return resume_data
    except Exception as e:
        raise ValueError(f"Error evaluating resume_data string: {str(e)}")

def find_key(resume_data, search_terms):
    """
    Find a key in the resume_data dictionary that matches any of the search_terms.
    """
    for key in resume_data.keys():
        if any(term.lower() in key.lower() for term in search_terms):
            return resume_data[key]
    return "Not available"

def process_resumes_in_folder(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Processing file: {pdf_file}")
        
        resume_text = extract_text_from_pdf(pdf_path)

        context = resume_text + """
        Given the following resume text, extract the following entities and organize them as a dictionary with keys: Name, Email, Mobile number, Experience in years (Mark Zero if a fresher), Top 5 technical skills mentioned, College name, Year of passout, Degree, Branch, Known language, current location and probability of moving to Coimbatore. Make sure it has the following keys: Name, Email, Mobile number, Experience in years, Top 5 technical skills, College name, Year of passout, Degree, Branch, Known language, current location, and add similarity scores each as new fields for Data Engineering/SQL/ETL, Web Development/Full Stack Development, Testing, Dev Ops, and resume strength based on industry level of a fresher."""

        genai.configure(api_key=os.environ["API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(context)

        try:
            resume_data = process_resume_data(response.text)
            
            print("Name:", find_key(resume_data, ["Name"]))
            print("Email:", find_key(resume_data, ["Email"]))
            print("Mobile number:", find_key(resume_data, ["Mobile number"]))
            print("Experience in years:", find_key(resume_data, ["Experience in years"]))
            print("Probability of moving to Coimbatore:", find_key(resume_data, ["Probability of moving to Coimbatore"]))
            print("Top 5 technical skills:", find_key(resume_data, ["Top 5 technical skills"]))
            print("Similarity Scores:")
            print("- Data Engineering/SQL/ETL:", find_key(resume_data, ["Data Engineering/SQL/ETL"]))
            print("- Web Development/Full Stack Development:", find_key(resume_data, ["Web Development/Full Stack Development"]))
            print("- Testing:", find_key(resume_data, ["Testing"]))
            print("- Dev Ops:", find_key(resume_data, ["Ops"]))
            print("Resume strength:", find_key(resume_data, ["Resume Strength", "resume strength", "Strength"]))
            
        except Exception as e:
            print(f"Error processing resume data: {str(e)}")

        print("\n" + "-"*80 + "\n")

# Folder path containing the PDFs
folder_path = "/Users/krishnaprasath/Desktop/resumes"
process_resumes_in_folder(folder_path)

