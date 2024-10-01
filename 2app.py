import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables (if needed)
load_dotenv()

# Background styling
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
 background-image: url("https://e0.pxfuel.com/wallpapers/219/656/desktop-wallpaper-purple-color-background-best-for-your-mobile-tablet-explore-color-cool-color-colored-background-one-color-aesthetic-one-color.jpg");
# background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRA8091BboriqPexW4fpcLjeVsFTVLsseIN-3K_0hoTZEBvONQn9KBYFIL73NqLM79TXxU&usqp=CAU");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
# Synonym dictionary to map abbreviations and variations to standard terms
synonym_dict = {
    'js': 'javascript',
    'javascript': 'javascript',
    'py': 'python',
    'python': 'python',
    'cn': 'networking',
    'computer networking': 'networking',
    'networking': 'networking',
    'aws': 'aws',
    'ml': 'machine learning',
    'machine learning': 'machine learning',
    'data science': 'data science', 'ds':'data science',
    'sql': 'sql','SQL': 'sql', 
    # Add more synonyms as needed
}

# Function to normalize skills using the synonym dictionary
def normalize_skill(skill):
    skill_lower = skill.lower().strip()
    return synonym_dict.get(skill_lower, skill_lower)  # Return normalized or original if not found

# Function to extract and normalize skills from text
def extract_normalized_skills(text):
    skills_keywords = ['javascript', 'python', 'networking', 'sql', 'machine learning', 'data science', 'aws']
    found_skills = []
    for skill in skills_keywords:
        normalized_skill = normalize_skill(skill)
        if normalized_skill.lower() in text.lower():
            found_skills.append(normalized_skill)
    return found_skills

# Function to calculate cosine similarity between two text bodies
def calculate_similarity(resume_text, jd_text):
    # Create a TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Convert both the resume and job description to vectors
    vectors = vectorizer.fit_transform([resume_text, jd_text])

    # Calculate cosine similarity between the two vectors
    similarity = cosine_similarity(vectors)[0][1]
    
    return similarity * 100  # Convert to percentage

# Function to extract location from the resume or job description
def extract_location(text):
    # Example locations, you can add more or extract from the text dynamically
    locations = ['new york', 'california', 'san francisco', 'los angeles', 'texas','maharashtra','bengaluru']
    for location in locations:
        if location.lower() in text.lower():
            return location
    return None

# Function to calculate percentage match based on found and required items
def calculate_match_percentage(found_items, required_items):
    if len(required_items) == 0:
        return 0
    matched_items = set(found_items).intersection(set(required_items))
    return (len(matched_items) / len(required_items)) * 100

# Streamlit app setup
st.title("SMART APPLICATION TRACKING SYSTEM")
st.text("Improve Your Resume ATS Score")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        # Extract text from the PDF resume
        reader = pdf.PdfReader(uploaded_file)
        extracted_text = ""
        for page in range(len(reader.pages)):
            extracted_text += str(reader.pages[page].extract_text() or "")
        
        # Normalize and extract skills from resume and JD
        resume_skills = extract_normalized_skills(extracted_text)
        jd_skills = extract_normalized_skills(jd)
        
        # Calculate skills match percentage
        skills_match_percentage = calculate_match_percentage(resume_skills, jd_skills)
        
        # Calculate experience similarity using cosine similarity
        experience_match_percentage = calculate_similarity(extracted_text, jd)
        
        # Extract locations and calculate location match
        resume_location = extract_location(extracted_text)
        jd_location = extract_location(jd)
        location_match_percentage = 100 if resume_location and resume_location == jd_location else 0

        # Output results
        st.write(f"• Skills Match Percentage: {skills_match_percentage:.2f}%")
        st.write(f"• Experience Match Percentage: {experience_match_percentage:.2f}%")
        st.write(f"• Location Match Percentage: {location_match_percentage}%")
        st.write(f"• Resume Skills: {', '.join(resume_skills)}")
        st.write(f"• Job Description Skills: {', '.join(jd_skills)}")
        st.write(f"• Resume Location: {resume_location if resume_location else 'Not Found'}")
        st.write(f"• Job Description Location: {jd_location if jd_location else 'Not Specified'}")
