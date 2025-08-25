### AI-powered fact-checking multi agent system built using Google ADK 

### Overview
This system uses a pipeline of specialized AI agents to methodically check a claim:
1.  **Web Search Agent:** Scours the internet for the most relevant and credible sources.
2.  **Web Scrap Agent:** Extracts and cleans the core content from the resulting articles.
3.  **Fact Check Agent:** Analyzes the compiled evidence using Gemini to render a final, reasoned verdict.

### Prerequisites

-   A Google AI API Key ([Get one here](https://aistudio.google.com/))
-   A SearchAPI.io or SerpApi account (for web search) ([Get one here](https://www.searchapi.io/))
-   A Firecrawl account (for web scraping) ([Get one here](https://www.firecrawl.dev/))

### Getting started
1.  **Clone the repo**
    ```bash
    git clone https://github.com/rajaravindp/gitThemFacts.git
    cd gitThemFacts
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up environment variables**
    Copy the `.env.example` file to `.env` and fill in your API keys:
    ```bash
    cp .env.example .env
    ```
    Edit `.env`:
    ```ini
    GOOGLE_API_KEY=your_google_ai_api_key_here
    SEARCH_API_KEY=your_searchapi_key_here
    FIRECRAWL_API_KEY=your_firecrawl_key_here
    ```

4.  **Run the agent**
    ```bash
    adk web
    ```

### Workflow
![Fact-checking workflow diagram](/workflow.png)