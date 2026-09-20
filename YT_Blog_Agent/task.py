from crewai import Task
from tools import yt_tool
from agents import blog_researcher, blog_writer

research_task = Task(
	description=(
		"Identify the video {topic}."
		"Get detailed information about the video from the channel"
	),
	expected_output='A comprehensive 3 paragraph long report based on the {topic} of video from the channel',
	tools=[yt_tool],
	agent=blog_researcher,
)

writer_task = Task(
	description=(
		"Get the information from the youtube channel on the topic {topic}"
	),
	expected_output='Summarize the information from the youtube channel video on the topic {topic} in a compelling blog post format',
	tools=[yt_tool],
	agent=blog_writer,
	async_execution=False,
	output_file='new-blog-post.md'
)
