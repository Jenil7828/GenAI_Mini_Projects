from crewai import Agent
from tools import yt_tool
from crewai import LLM
import os

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

blog_researcher = Agent(
	role='Blog Researcher from Youtube videos',
	goal='Get the relevant video content for the topic {topic} from YouTube Channel',
	verbose=True,
	memory=False,
	backstory = (
		"Expert in understanding videos in AI Data Science, Machine Learning and GEN AI and providing suggestion"
	),
	tools=[yt_tool],
	llm=llm,
	# function_calling_llm=llm,
	allow_delegation=True
)

blog_writer = Agent(
role='Blog Writer',
	goal='Narrate compelling tech stories about the video {topic} from YouTube Channel',
	verbose=True,
	memory=False,
	backstory = (
		"With a flair for simplifying complex topics, you craft engaging narratives that captivate and educate, bringing new discoveries to light in an accessible manner"
	),
	tools=[yt_tool],
	llm=llm,
	# function_calling_llm=llm,
	allow_delegation=False
)