"""
Example Workflow #2: Automated Code Review

This workflow demonstrates:
1. Voice command to review code
2. Code agent analyzes the code
3. Validator agent checks for issues
4. Report generated with suggestions
"""

import asyncio
from backend.app.agents.main_agent import MainAgent
from backend.app.agents.base import Task


async def code_review_workflow():
    """
    Execute an automated code review workflow.
    
    Voice Command: "Review the code in the utils directory"
    """
    print("=" * 80)
    print("Workflow #2: Automated Code Review")
    print("=" * 80)
    print()
    
    # Create main agent
    main_agent = MainAgent()
    
    # Create code review task
    task = Task(
        type="code_review",
        description="Review Python code for best practices and potential issues",
        params={
            "target_path": "./backend/app/agents",
            "checks": [
                "code_quality",
                "security",
                "performance",
                "best_practices",
            ],
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
    asyncio.run(code_review_workflow())

