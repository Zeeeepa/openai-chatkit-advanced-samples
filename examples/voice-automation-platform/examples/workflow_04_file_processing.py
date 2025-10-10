"""
Example Workflow #4: Batch File Processing

This workflow demonstrates:
1. Voice command to process files
2. File manager tool lists files
3. Code agent processes each file
4. Results compiled and validated
"""

import asyncio
from backend.app.agents.main_agent import MainAgent
from backend.app.agents.base import Task


async def file_processing_workflow():
    """
    Execute a batch file processing workflow.
    
    Voice Command: "Process all JSON files in the data directory and extract key insights"
    """
    print("=" * 80)
    print("Workflow #4: Batch File Processing")
    print("=" * 80)
    print()
    
    # Create main agent
    main_agent = MainAgent()
    
    # Create file processing task
    task = Task(
        type="file_processing",
        description="Process JSON files and extract insights",
        params={
            "directory": "./data",
            "file_pattern": "*.json",
            "operation": "extract_insights",
            "output_file": "./results/insights.json",
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
    asyncio.run(file_processing_workflow())

