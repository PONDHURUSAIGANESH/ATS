# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai
import PyPDF2 as pdf
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.getenv("AIzaSyCuMjpOaP053744ZZI_qWIbdHxtsNvh3aw"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

@app.route('/evaluate', methods=['POST', 'OPTIONS'])
def evaluate_resume():
    if request.method == 'OPTIONS':
        response = app.make_default_options_response()
    else:
        jd = request.form.get('jd', '')  # Use get method with a default value
        resume = request.files['resume']
        input_prompt ="""

        ### As a skilled Application Tracking System (ATS) with advanced knowledge in technology and data science, your role is to meticulously evaluate a candidate's resume based on the provided job description. 

        ### Your evaluation will involve analyzing the resume for relevant skills, experiences, and qualifications that align with the job requirements. Look for key buzzwords and specific criteria outlined in the job description to determine the candidate's suitability for the position.

        ### Provide a detailed assessment of how well the resume matches the job requirements, highlighting strengths, weaknesses, and any potential areas of concern. Offer constructive feedback on how the candidate can enhance their resume to better align with the job description and improve their chances of securing the position.

        ### Your evaluation should be thorough, precise, and objective, ensuring that the most qualified candidates are accurately identified based on their resume content in relation to the job criteria.

        ### Remember to utilize your expertise in technology and data science to conduct a comprehensive evaluation that optimizes the recruitment process for the hiring company. Your insights will play a crucial role in determining the candidate's compatibility with the job role.
        resume={text}
        jd={jd}
        1. Calculate the percentage of match between the resume and the job description. Give a number and some explation
        2. Identify any key keywords that are missing from the resume in comparison to the job description.
        3. Offer specific and actionable tips to enhance the resume and improve its alignment with the job requirements.
        """
                
        text = input_pdf_text(resume)
        response = get_gemini_response(input_prompt.format(text=text, jd=jd))

    return jsonify({'result': response})

if __name__ == '__main__':
    app.run(debug=True)
