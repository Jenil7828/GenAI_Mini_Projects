import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = "You are Youtube video summarizer. you will be taking the transcript text and summarizing thee entire video and providing important summary in points within 250 words. The Transcript will be appended here:\n"

def get_response(transcript_text, prompt):
	model = genai.GenerativeModel("models/gemini-2.5-flash")
	response = model.generate_content(prompt+transcript_text)
	return response.text

def fetch_transcript(youtube_url):
	try:
		video_id = youtube_url.split("=")[1]
		transcript_text = YouTubeTranscriptApi().fetch(video_id)
		transcript = ''
		for i in transcript_text:
			transcript+= " "+i.text
		return transcript
	except Exception as e:
		raise e


st.set_page_config(page_title="YT Transcript Summarizer")
yt_link = st.text_input("Enter Video Link ", key="input")
if yt_link:
	video_id = yt_link.split("=")[1]
	st.image(f"http://ikmg/youtube.com/vi/{video_id}/0.jpg", width="stretch")


if st.button("Summarize"):
	transcript_text = fetch_transcript(yt_link)
	if transcript_text:
		response = get_response(transcript_text, prompt)
		st.markdown("## Detailed Notes:  ")
		st.write(response)
