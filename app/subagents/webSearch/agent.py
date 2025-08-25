import os
from dotenv import load_dotenv
import requests
from typing import Dict

from . import prompt

from google.adk.agents import Agent

load_dotenv()
search_url = "https://www.searchapi.io/api/v1/search"
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")

# Web search tool
def web_search(query: str) -> Dict:
    """Searches the web for current information using SearchAPI.
     Args:
        query: The search query string.

    Returns:
        A dictionary containing the search results with title, URL, and description.
    """
    print(f"--- Tool: web_search called for query: {query} ---")

    try:
        response = requests.get(search_url,
                                params={
                                    "engine": "google",
                                    "q": query,
                                    "num": 5,
                                    "api_key": "aRdkSfLsdV5yZ4tqXKRj5i5r",
                                })
        response.raise_for_status() 
        data = response.json()
        
        formatted_results = []
        for item in data.get('organic_results', []):
            formatted_results.append({
                "title": item.get("title", "No title"),
                "url": item.get("link", "No URL"),
                "description": item.get("snippet", "No description"),
            })
        
        return {
            "status": "success",
            "results": formatted_results
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error_message": f" Error fetching web search results: \n Error: {str(e)}"
        }

# Web search agent
web_search_agent = Agent(
    model=MODEL_GEMINI_2_0_FLASH,
    name="web_search_agent",
    instruction=prompt.WEB_SEARCH_PROMPT,
    description="Searches web for relevant information and returns a list of URLs using the web_search tool.",
    tools=[web_search]
)