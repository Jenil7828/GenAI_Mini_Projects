import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_response(input_promt, image):
	model = genai.GenerativeModel("models/gemini-2.5-flash")
	response = model.generate_content([input_promt, image[0]])
	return response.text

def input_image_setup(file):
	if file is not None:
		bytes_data = file.getvalue()
		image_parts = [
			{
				"mime_type": file.type,
				"data": bytes_data
			}
		]
		return image_parts
	else:
		raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="Calories Advisor App")
# input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice..", type=['jpeg', 'png', 'jpg'])
image = ""
if uploaded_file is not None:
	image= Image.open(uploaded_file)
	st.image(image, caption="Uploaded Image.", width="stretch")

submit = st.button("Tell me about the total calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image and calculate the total calories.
Also provide a detailed of every food items with the calorie intake in the below format 
1. Item 1 - number of calories
2. Item 2 - number of calories
----
----

Finally, you can also mention whether the food is healthy or not and also mention the percentage split of ratio of carbohydrate, fats, fiber, sugar, and other important things that is required in our diet.
"""

if submit:
	image_data = input_image_setup(uploaded_file)
	response = get_response(input_prompt, image_data)
	st.subheader("The response is ")
	st.write(response)