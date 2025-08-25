from google.adk.agents import SequentialAgent, Agent

from .subagents.webSearch import web_search_agent
from .subagents.webScrap import web_scrap_agent
from .subagents.deepResearch import deep_research_agent

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
claim_extraction_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="claim_extraction_agent",
    instruction="Extract the factual claim from the user input and return it as a clean string.",
    description="Extracts the core claim from user input for fact-checking"
)

final_agent = SequentialAgent(
    name='Factual_Information_Checking_Agent',
    description=(
        """
        This agent is responsible for fact-checking information by cross-referencing 
        claims with reliable sources and evidence.
        """
    ),
    sub_agents=[claim_extraction_agent, web_search_agent, web_scrap_agent, deep_research_agent]
)

root_agent = final_agent