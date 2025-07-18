import wikipedia
from crewai import Agent, Crew, Process, Task
from crewai.tools import BaseTool as CrewAITool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from observability import setup_observability
from pydantic import Field

setup_observability()


class SearchTool(CrewAITool):
    name: str = "Search"
    description: str = (
        "Useful for search-based queries. Use this to find current information about markets, companies, and trends."
    )
    search: DuckDuckGoSearchRun = Field(default_factory=DuckDuckGoSearchRun)

    def _run(self, query: str) -> str:
        """Execute the search query and return results"""
        try:
            return self.search.run(query)
        except Exception as e:
            return f"Error performing search: {str(e)}"


class WikipediaToolWrapper(CrewAITool):
    name: str = "Wikipedia Search"
    description: str = "Search Wikipedia for factual information"
    langchain_tool: WikipediaQueryRun = Field(
        default_factory=lambda: WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper(wiki_client=wikipedia))
    )

    def _run(self, query: str) -> str:
        """Execute the Wikipedia search query and return results"""
        try:
            return self.langchain_tool._run(query)
        except Exception as e:
            return f"Error performing Wikipedia search: {str(e)}"


# Wrap LangChain tools for CrewAI
crewai_search_tool = SearchTool()
crewai_wikipedia_tool = WikipediaToolWrapper()

researcher = Agent(
    role="Senior Research Analyst",
    goal="Uncover cutting-edge developments in AI and data science",
    backstory="""You are a seasoned Research Analyst, specializing in AI and data science.""",
    verbose=True,
    allow_delegation=False,
    # You can pass an optional llm attribute specifying what model you wanna use.
    # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7),
    tools=[crewai_wikipedia_tool, crewai_search_tool],
)
writer = Agent(
    role="Tech Content Strategist",
    goal="Craft compelling content on tech advancements",
    backstory="""You are a renowned Content Strategist, known for your insightful and engaging articles.
  You transform complex concepts into compelling narratives.""",
    verbose=True,
    allow_delegation=True,
)

# Create tasks for your agents
task1 = Task(
    description="""Conduct a comprehensive analysis of the latest advancements in AI in 2024.
  Identify key trends, breakthrough technologies, and potential industry impacts.""",
    expected_output="Full analysis report in bullet points",
    agent=researcher,
)

task2 = Task(
    description="""Using the insights provided, develop an engaging blog
  post that highlights the most significant AI advancements.
  Your post should be informative yet accessible, catering to a tech-savvy audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI.""",
    expected_output="Full blog post of at least 4 paragraphs",
    agent=writer,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    # verbose=2, # You can set it to 1 or 2 to different logging levels
    process=Process.sequential,
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
