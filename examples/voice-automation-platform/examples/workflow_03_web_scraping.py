"""
Example Workflow #3: Web Scraping and Analysis

This workflow demonstrates:
1. Voice command to scrape websites
2. Research agent finds relevant URLs
3. Web search tool extracts data
4. Code agent processes and analyzes data
"""

import asyncio
from backend.app.agents.main_agent import MainAgent
from backend.app.agents.base import Task


async def web_scraping_workflow():
    """
    Execute a web scraping and analysis workflow.
    
    Voice Command: "Scrape the latest AI news from TechCrunch and summarize"
    """
    print("=" * 80)
    print("Workflow #3: Web Scraping and Analysis")
    print("=" * 80)
    print()
    
    # Create main agent
    main_agent = MainAgent()
    
    # Create web scraping task
    task = Task(
        type="web_scraping",
        description="Scrape latest AI news and create a summary",
        params={
            "target_site": "TechCrunch",
            "topic": "artificial intelligence",
            "max_articles": 10,
            "analysis_type": "summary",
            "output_format": "json",
        },
    )
    
    print(f"📋 Task Created: {task.id}")
    print(f"📝 Description: {task.description}")
    print()
    
    # Execute task
    print("🚀 Executing task...")
    result = await main_agent.process_task(task)
    
    print()
    print("=" * 80)
    print("✅ Workflow Complete!")
    print("=" * 80)
    print()
    print(f"Result: {result}")
    
    return result


if __name__ == "__main__":
    # Run the workflow
    asyncio.run(web_scraping_workflow())

