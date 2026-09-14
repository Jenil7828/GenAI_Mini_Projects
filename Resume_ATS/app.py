from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
import pdf2image
from PyPDF2 import PdfReader

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
	model=genai.GenerativeModel("models/gemini-2.5-flash")
	response = model.generate_content(f"""
        {input}

        Resume:
        {pdf_content}

        Job Description:
        {prompt}
        """
									  )
	return response.text

# def input_pdf_setup(uploaded_file):
# 	if uploaded_file is not None:
# 		images=pdf2image.convert_from_bytes(uploaded_file.read())
# 		first_page = images[0]
# 		img_byte_arr = io.BytesIO()
# 		first_page.save(img_byte_arr, format="JPEG")
# 		img_byte_arr= img_byte_arr.getvalue()
# 		pdf_parts = [
# 			{
# 				"mime_type": "image/jpeg",
# 				"data": base64.b64encode(img_byte_arr).decode()
# 			}
# 		]
# 		return pdf_parts
# 	else:
# 		raise FileNotFoundError("NOt found")
def input_pdf_setup(uploaded_file):
	if uploaded_file is not None:
		reader = PdfReader(uploaded_file)

		text = ""

		for page in reader.pages:
			text += page.extract_text() or ""

		return text

	else:
		raise FileNotFoundError("Not found")

st.set_page_config(page_title="ats")
st.header('ATS Tracker')
input_text = st.text_input("Job description", key='input')
uploaded_file= st.file_uploader("Upload your Resume", type=["pdf"])
if uploaded_file is not None:
	st.write("File uploaded")

submit1 = st.button("Tell me about the Resume")
submit2 = st.button("How can I improve my skills")
submit3 = st.button("Percentage Match")

input_prompt_1 = """
you are an experienced HR with tech experience in the field of AI, full stack, web development, big data engineering, devops, data analyst your task is to review the provided resume against the job description.
Please share your professional evaluation on whether the candidate's profile aligns with the JD.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirement.
"""

input_prompt_2 = """
you are an experienced HR with tech experience in the field of AI, full stack, web development, big data engineering, devops, data analyst your role is to scrutinize the resume in light of the job description provided.
share your insights on the candidate's suitability for the role from an HR perspective.
Additionally, offer advice on enhancing the candidate's skills and identify the missing skills required for the job 
"""

input_prompt_3= """
you are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of AI, full stack, web development, big data engineering, devops, data analyst and deep ATS functionality,
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches the  job description. First the output should come as percentage and then keywords missing in the resume and last final thoughts
"""
if submit1:
	if uploaded_file is not None:
		pdf_content = input_pdf_setup(uploaded_file)
		response = get_gemini_response(input_prompt_1, pdf_content, input_text)
		st.subheader("the resposne is:\n")
		st.write(response)

	else:
		st.write("Please upload resume")
elif submit2:
	if uploaded_file is not None:
		pdf_content = input_pdf_setup(uploaded_file)
		response = get_gemini_response(input_prompt_2, pdf_content, input_text)
		st.subheader("the resposne is:\n")
		st.write(response)

	else:
		st.write("Please upload resume")
elif submit3:
	if uploaded_file is not None:
		pdf_content = input_pdf_setup(uploaded_file)
		response = get_gemini_response(input_prompt_3, pdf_content, input_text)
		st.subheader("the resposne is:\n")
		st.write(response)

	else:
		st.write("Please upload resume")