from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(question, prompt):
	model = genai.GenerativeModel("models/gemini-2.5-flash")
	response = model.generate_content([prompt, question])
	return response.text

def read_sql_query(sql, db):
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	cur.execute(sql)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	for row in rows:
		print(row)
	return rows

prompt="""
	You are an expert in converting English questions to SQL query!
	The SQL databases has the name STudent and has the following columns -NAME, CLASS, SECTION, MARKS \n\nFor example, 
	Example 1 - How many entries are persent?, the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
	Example 2 - Tell me about the students studying in AI class?, the SQL command will be something like this SELECT * FROM STUDENT where CLASS='AI';
	also the sql code should not have ``` in beginning or end and sql word in the output
	"""

st.set_page_config(page_title="Any SQL Command")
st.header("Gemini app to retrieve SQL Data")
question = st.text_input("Input", key='input')
submit = st.button("Ask the question")
if submit:
	response = get_gemini_response(question, prompt)
	print(response)
	data = read_sql_query(response, "student.db")
	st.subheader("The response is ")
	for row in data:
		print(row)
		st.write(row)