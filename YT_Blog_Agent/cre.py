from crewai import Crew, Process
from agents import blog_researcher, blog_writer, llm
from task import research_task, writer_task

crew = Crew(
	agents=[blog_researcher, blog_writer],
	tasks=[research_task, writer_task],
	process=Process.sequential,
	memory=False,
	cache=True,
	max_rpm=100,
	share_crew=True,
	# function_calling_llm=llm
)

result = crew.kickoff(inputs={'topic': 'AI VS ML VS DL vs Data Science'})
print(result)