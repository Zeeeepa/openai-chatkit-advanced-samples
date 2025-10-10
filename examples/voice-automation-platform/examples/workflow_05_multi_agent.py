"""
Example Workflow #5: Multi-Agent Collaboration

This workflow demonstrates:
1. Complex voice command requiring multiple agents
2. Research agent gathers requirements
3. Code agent implements solution
4. Validator agent tests and validates
5. Orchestrator coordinates all agents
"""

import asyncio
from backend.app.agents.main_agent import MainAgent
from backend.app.agents.base import Task


async def multi_agent_workflow():
    """
    Execute a complex multi-agent collaboration workflow.
    
    Voice Command: "Create a REST API for a todo application with tests"
    """
    print("=" * 80)
    print("Workflow #5: Multi-Agent Collaboration")
    print("=" * 80)
    print()
    
    # Create main agent
    main_agent = MainAgent()
    
    # Create complex task requiring multiple agents
    task = Task(
        type="multi_agent_project",
        description="Create a complete REST API for a todo application with full test coverage",
        params={
            "project_type": "REST API",
            "features": [
                "CRUD operations for todos",
                "User authentication",
                "Database integration",
                "Input validation",
            ],
            "requirements": [
                "FastAPI framework",
                "SQLAlchemy ORM",
                "Pytest for testing",
                "Full API documentation",
            ],
            "output_directory": "./output/todo_api",
        },
        priority=8,  # High priority
    )
    
    print(f"📋 Task Created: {task.id}")
    print(f"📝 Description: {task.description}")
    print(f"⚡ Priority: {task.priority}/10")
    print()
    
    # Execute task (will spawn multiple sub-agents)
    print("🚀 Executing task...")
    print("   This will coordinate multiple agents:")
    print("   - Research Agent: Gathers requirements and best practices")
    print("   - Code Agent: Implements the API")
    print("   - Validator Agent: Tests and validates the implementation")
    print()
    
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
    asyncio.run(multi_agent_workflow())

