"""
Example Workflow #1: Research and Report Generation

This workflow demonstrates:
1. Voice command to trigger research
2. Research agent gathers information
3. Code agent generates report
4. Validator agent checks quality
"""

import asyncio
from backend.app.agents.main_agent import MainAgent
from backend.app.agents.base import Task


async def research_report_workflow():
    """
    Execute a complete research and report generation workflow.
    
    Voice Command: "Research the latest trends in AI agents and create a report"
    """
    print("=" * 80)
    print("Workflow #1: Research and Report Generation")
    print("=" * 80)
    print()
    
    # Create main agent
    main_agent = MainAgent()
    
    # Create research task
    task = Task(
        type="research_report",
        description="Research the latest trends in AI agents and create a comprehensive report",
        params={
            "topic": "AI agents",
            "focus_areas": ["architecture", "tools", "use_cases"],
            "output_format": "markdown",
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
    asyncio.run(research_report_workflow())

