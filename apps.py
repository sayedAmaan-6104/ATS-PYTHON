import os
import PyPDF2 as pdf
import streamlit as st
from dotenv import load_dotenv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the environment variables
load_dotenv('ammo.env')

st.set_page_config(page_title="Smart Application Tracking System", page_icon=":robot:")

# Background styling
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://e0.pxfuel.com/wallpapers/219/656/desktop-wallpaper-purple-color-background-best-for-your-mobile-tablet-explore-color-cool-color-colored-background-one-color-aesthetic-one-color.jpg");
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

# Streamlit app UI
st.title("SMART APPLICATION TRACKING SYSTEM")
st.text("Improve Your Resume ATS Score")
jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

submit = st.button("Submit")

# Helper functions
def calculate_cosine_similarity(text1, text2):
    """Calculate cosine similarity between two pieces of text."""
    vectorizer = CountVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0][1] * 100

def extract_skills(text):
    """Extract skills from a resume or job description."""
    skills_keywords = ['Python', 'Java', 'SQL', 'Machine Learning', 'Data Analysis', 'Big Data', 'AWS', 'Git', 'Docker', 'Kubernetes']
    found_skills = [skill for skill in skills_keywords if skill.lower() in text.lower()]
    return found_skills

def calculate_match_percentage(found_items, required_items):
    """Calculate percentage match between found and required items."""
    if len(required_items) == 0:
        return 0
    matched_items = set(found_items).intersection(set(required_items))
    return (len(matched_items) / len(required_items)) * 100

if submit:
    if uploaded_file is not None:
        # Extract text from the PDF resume
        reader = pdf.PdfReader(uploaded_file)
        extracted_text = ""
        for page in range(len(reader.pages)):
            extracted_text += str(reader.pages[page].extract_text() or "")
        
        # Extract skills from resume and job description
        resume_skills = extract_skills(extracted_text)
        jd_skills = extract_skills(jd)
        
        # Calculate skills matching percentage
        skills_match_percentage = calculate_match_percentage(resume_skills, jd_skills)
        
        # Calculate experience matching using cosine similarity (simplified for demo purposes)
        experience_match_percentage = calculate_cosine_similarity(extracted_text, jd)
        
        # For location matching (example based, checks if resume contains the location string from JD)
        location_in_resume = 'New York'  # You can extend this by actually extracting location from resume.
        location_in_jd = 'New York'  # Extend to extract location from JD if needed
        location_match_percentage = 100 if location_in_jd.lower() in extracted_text.lower() else 0
        
        # Calculate missing keywords
        missing_keywords = set(jd_skills) - set(resume_skills)
        
        # Profile Summary
        profile_summary = f"Skills: {', '.join(resume_skills)} | Location: {location_in_resume}"

        # Display the results
        st.write(f"• Skills Match Percentage: {skills_match_percentage:.2f}%")
        st.write(f"• Experience Match Percentage: {experience_match_percentage:.2f}%")
        st.write(f"• Location Match Percentage: {location_match_percentage}%")
        st.write(f"• Missing Keywords: {', '.join(missing_keywords)}")
        st.write(f"• Profile Summary: {profile_summary}")
