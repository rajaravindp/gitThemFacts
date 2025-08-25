import os
import json
from dotenv import load_dotenv
from typing import Dict

from google import genai
from google.adk.agents import Agent

from . import prompt

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"

# Deep research tool
def deep_research(evidence: dict) -> Dict:
    """
    Checks the validity of a claim against provided evidence.

    Args:
        claim (str): The claim to be checked.
        evidence (dict): The evidence to check the claim against.

    Returns:
        Dict: A dictionary containing the result of the fact-checking.
    """
    print(f"--- Tool: deep_research called ---")
    try: 
        llm = genai.Client(api_key=GOOGLE_API_KEY)
        chat = llm.chats.create(model=MODEL_GEMINI_2_0_FLASH)

        result = {"messages": []}
        for chunk in chat.send_message_stream(
            message=f"""
            Analyze the claim against the provided evidence and provide fact-checking verdicts:
                
                CLAIM TO VERIFY:
                claim

                EVIDENCE:
                {json.dumps(evidence, indent=2)}

                For each claim, provide:
                1. Verdict: True, False, Partially True, or Unverifiable
                2. Confidence Level: High, Medium, Low
                3. Key evidence supporting the verdict
                4. Source citations
                5. Explanation of reasoning
                
            Return the response in structured JSON format.
                """
        ):
            result["messages"].append(chunk)

        return result
    except Exception as e:
        print(f"Error occurred: {e}")
        return {"error": str(e)}

# Fact checker agent
deep_research_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="deep_research_agent",
    instruction=prompt.FACT_CHECK_PROMPT,
    description="Conducts deep, comprehensive research fact-check claim using multiple sources with the deep_research tool.",
    tools=[deep_research]
)
