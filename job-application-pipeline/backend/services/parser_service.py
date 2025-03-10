import PyPDF2
import docx
import re
import os

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_cv_data(file_path):
    # Extract text based on file type
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
    
    # Simple regex-based extraction
    # This is a basic implementation - in a production environment, 
    # you would want to use more sophisticated ML/NLP techniques
    
    cv_data = {
        "personal_info": {},
        "education": [],
        "qualifications": [],
        "projects": []
    }
    
    # Extract personal info
    name_match = re.search(r'^([\w\s]+)', text.strip())
    if name_match:
        cv_data["personal_info"]["name"] = name_match.group(1).strip()
    
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    if email_match:
        cv_data["personal_info"]["email"] = email_match.group(0)
    
    phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4})', text)
    if phone_match:
        cv_data["personal_info"]["phone"] = phone_match.group(0)
    
    # Extract education
    education_section = re.search(r'(?i)education[:\s]*(.*?)(?=qualifications|projects|experience|skills|$)', text, re.DOTALL)
    if education_section:
        education_text = education_section.group(1).strip()
        education_entries = re.split(r'\n\n+', education_text)
        for entry in education_entries:
            if entry.strip():
                cv_data["education"].append(entry.strip())
    
    # Extract qualifications
    qualifications_section = re.search(r'(?i)qualifications[:\s]*(.*?)(?=education|projects|experience|skills|$)', text, re.DOTALL)
    if qualifications_section:
        qualification_text = qualifications_section.group(1).strip()
        qualification_entries = re.split(r'\n\n+', qualification_text)
        for entry in qualification_entries:
            if entry.strip():
                cv_data["qualifications"].append(entry.strip())
    
    # Extract projects
    projects_section = re.search(r'(?i)projects[:\s]*(.*?)(?=education|qualifications|experience|skills|$)', text, re.DOTALL)
    if projects_section:
        projects_text = projects_section.group(1).strip()
        project_entries = re.split(r'\n\n+', projects_text)
        for entry in project_entries:
            if entry.strip():
                cv_data["projects"].append(entry.strip())
    
    return cv_data