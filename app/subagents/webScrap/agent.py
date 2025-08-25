import os
from dotenv import load_dotenv
from typing import Dict
from urllib.parse import urlparse

from . import prompt

from google.adk.agents import Agent
from firecrawl import FirecrawlApp

load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
    
# Web scrap tool
def web_scrap(search_results: dict, extract_format: str) -> Dict:
    """
    Scrapes the web content from URLs found in the web search results using firecrawl.
    
    Args:
        search_results: The formatted results from the web search agent
        extract_format (str): Format to extract ('markdown', 'html', or 'links').
        
    Returns:
        Dict: A dictionary containing the scraped content.
    """
    print(f"--- Tool: web_scrap called ---")

    urls = []
    if isinstance(search_results, dict):
        if "results" in search_results:
            # Handle your web_search tool format
            for result in search_results["results"]:
                if isinstance(result, dict) and "url" in result:
                    urls.append(result["url"])
        else:
            urls = list(search_results.values()) if isinstance(search_results, dict) else search_results

    try: 
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        web_content = {}
        formats = [extract_format] 

        for url in urls:
            try:
                result = app.scrape(url, formats=formats)
                
                if extract_format == "markdown" and hasattr(result, "markdown"):
                    content = result.markdown
                elif extract_format == "html" and hasattr(result, "html"):
                    content = result.html
                elif extract_format == "links" and hasattr(result, "links"):
                    content = result.links
                else:
                    content = f"Content not available in '{extract_format}' format"
                
                domain = urlparse(url).netloc
                
                metadata = getattr(result, "metadata", {})
                title = getattr(result, "title", None)
                if not title and metadata and "og_title" in metadata:
                    title = metadata["og_title"]
                if not title and not metadata:
                    title = "No title"
                
                web_content[url] = {
                    "domain": domain,
                    "format": extract_format,
                    "content": content,
                    "metadata": metadata,
                    "title": title
                }
                
                print(f"✓ Successfully scraped: {url}")
            except Exception as e:
                print(f"✗ Failed to scrape {url}: {str(e)}")
                web_content[url] = {"error": str(e)}

        return {
            "status": "success",
            "data": web_content
        }

    except Exception as e:
        return {"status": "error", "message": f"Error during web scraping: {str(e)}"}

web_scrap_agent = Agent(
    model="gemini-2.0-flash",
    name="web_scrap_agent",
    instruction=prompt.WEB_SCRAP_PROMPT,
    description="Scrapes web content from a list of URLs using the web_scrap tool.",
    tools=[web_scrap]
)