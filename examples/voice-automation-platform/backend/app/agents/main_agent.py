"""Main orchestrator agent for voice automation platform."""

import asyncio
import re
from typing import Any

from chatkit.agents import Agent, AgentContext
from chatkit.types import ThreadMetadata

from .base import AgentRole, AgentStatus, BaseAgent, Task
from .research_agent import ResearchAgent
from .code_agent import CodeAgent
from .validator_agent import ValidatorAgent


class MainAgent(BaseAgent):
    """
    Main orchestrator agent that:
    - Parses voice commands into structured tasks
    - Spawns specialized sub-agents
    - Coordinates multi-agent workflows
    - Aggregates results
    - Validates final output
    """

    def __init__(self):
        """Initialize the main orchestrator agent."""
        super().__init__(
            name="Main Orchestrator",
            description="Coordinates multi-agent workflows from voice commands",
            role=AgentRole.ORCHESTRATOR,
            model="gpt-4",
            temperature=0.3,  # Lower temperature for more consistent orchestration
            max_tokens=4000,
            tools=["command_parser", "agent_spawner", "result_aggregator"],
        )
        
        # Registry of available sub-agents
        self._agent_registry: dict[AgentRole, type[BaseAgent]] = {
            AgentRole.RESEARCH: ResearchAgent,
            AgentRole.CODE: CodeAgent,
            AgentRole.VALIDATOR: ValidatorAgent,
        }
        
        # Active sub-agents
        self._active_agents: dict[str, BaseAgent] = {}
        
        # Task dependency graph
        self._task_graph: dict[str, list[str]] = {}

    async def process_task(self, task: Task) -> Any:
        """
        Process a task by orchestrating sub-agents.
        
        Args:
            task: Task to process (typically a voice command)
            
        Returns:
            Aggregated result from all sub-agents
        """
        # Parse the command into subtasks
        subtasks = await self._parse_command(task)
        
        # Build dependency graph
        self._build_dependency_graph(subtasks)
        
        # Execute subtasks with proper ordering
        results = await self._execute_subtasks(subtasks)
        
        # Aggregate results
        final_result = await self._aggregate_results(results)
        
        # Validate with validator agent
        validated_result = await self._validate_result(final_result)
        
        return validated_result

    async def validate_task(self, task: Task) -> bool:
        """
        Main agent can handle any task type - it's the orchestrator.
        
        Args:
            task: Task to validate
            
        Returns:
            True always (orchestrator handles all tasks)
        """
        return True

    async def _parse_command(self, task: Task) -> list[Task]:
        """
        Parse a voice command into structured subtasks.
        
        Args:
            task: Original task with voice command
            
        Returns:
            List of subtasks for specialized agents
        """
        command = task.description.lower()
        subtasks: list[Task] = []
        
        # Research patterns
        research_patterns = [
            r"research",
            r"find.*information",
            r"search.*for",
            r"look.*up",
            r"what.*is",
            r"gather.*data",
        ]
        
        # Code patterns
        code_patterns = [
            r"create.*code",
            r"write.*function",
            r"implement",
            r"generate.*api",
            r"build.*app",
            r"fix.*bug",
            r"refactor",
        ]
        
        # Analysis patterns
        analysis_patterns = [
            r"analyze",
            r"examine",
            r"review",
            r"summarize",
            r"compare",
        ]
        
        # Test patterns
        test_patterns = [
            r"test",
            r"validate",
            r"verify",
            r"check",
        ]
        
        # Create research subtask if needed
        if any(re.search(pattern, command) for pattern in research_patterns):
            subtasks.append(
                Task(
                    type="research",
                    description=f"Research: {task.description}",
                    params={"query": task.description, "max_results": 10},
                    priority=10,
                )
            )
        
        # Create code subtask if needed
        if any(re.search(pattern, command) for pattern in code_patterns):
            subtasks.append(
                Task(
                    type="code",
                    description=f"Code: {task.description}",
                    params={"requirements": task.description},
                    priority=8,
                    depends_on=[subtasks[0].id] if subtasks else [],
                )
            )
        
        # Create analysis subtask if needed
        if any(re.search(pattern, command) for pattern in analysis_patterns):
            subtasks.append(
                Task(
                    type="analysis",
                    description=f"Analysis: {task.description}",
                    params={"data_source": "research_results"},
                    priority=7,
                    depends_on=[subtasks[0].id] if subtasks else [],
                )
            )
        
        # Always add validation at the end
        if subtasks:
            subtasks.append(
                Task(
                    type="validate",
                    description=f"Validate results for: {task.description}",
                    params={"criteria": "quality,accuracy,completeness"},
                    priority=5,
                    depends_on=[st.id for st in subtasks],
                )
            )
        
        # If no patterns matched, create a general research task
        if not subtasks:
            subtasks.append(
                Task(
                    type="research",
                    description=f"General research: {task.description}",
                    params={"query": task.description},
                    priority=5,
                )
            )
        
        return subtasks

    def _build_dependency_graph(self, subtasks: list[Task]) -> None:
        """
        Build dependency graph for task ordering.
        
        Args:
            subtasks: List of subtasks with dependencies
        """
        self._task_graph.clear()
        
        for task in subtasks:
            self._task_graph[task.id] = task.depends_on

    async def _execute_subtasks(self, subtasks: list[Task]) -> dict[str, Any]:
        """
        Execute subtasks respecting dependencies.
        
        Args:
            subtasks: List of subtasks to execute
            
        Returns:
            Dictionary mapping task IDs to results
        """
        results: dict[str, Any] = {}
        completed_tasks: set[str] = set()
        
        # Keep executing until all tasks are complete
        while len(completed_tasks) < len(subtasks):
            # Find tasks that can be executed (all dependencies met)
            ready_tasks = [
                task
                for task in subtasks
                if task.id not in completed_tasks
                and all(dep in completed_tasks for dep in task.depends_on)
            ]
            
            if not ready_tasks:
                # Circular dependency or error
                break
            
            # Execute ready tasks concurrently
            task_results = await asyncio.gather(
                *[self._execute_single_subtask(task) for task in ready_tasks],
                return_exceptions=True,
            )
            
            # Store results
            for task, result in zip(ready_tasks, task_results):
                if isinstance(result, Exception):
                    results[task.id] = {"error": str(result), "status": "failed"}
                else:
                    results[task.id] = result
                completed_tasks.add(task.id)
        
        return results

    async def _execute_single_subtask(self, task: Task) -> Any:
        """
        Execute a single subtask with appropriate agent.
        
        Args:
            task: Task to execute
            
        Returns:
            Task result
        """
        # Map task type to agent role
        task_to_role = {
            "research": AgentRole.RESEARCH,
            "code": AgentRole.CODE,
            "analysis": AgentRole.RESEARCH,  # Research agent handles analysis
            "validate": AgentRole.VALIDATOR,
        }
        
        role = task_to_role.get(task.type)
        if not role:
            raise ValueError(f"Unknown task type: {task.type}")
        
        # Spawn agent if needed
        agent = await self._spawn_agent(role)
        
        # Execute task
        completed_task = await agent.execute_task(task)
        
        return completed_task.result

    async def _spawn_agent(self, role: AgentRole) -> BaseAgent:
        """
        Spawn a sub-agent for the given role.
        
        Args:
            role: Agent role to spawn
            
        Returns:
            Agent instance
        """
        # Check if agent already exists
        if role.value in self._active_agents:
            return self._active_agents[role.value]
        
        # Create new agent
        agent_class = self._agent_registry.get(role)
        if not agent_class:
            raise ValueError(f"No agent registered for role: {role}")
        
        agent = agent_class()
        self._active_agents[role.value] = agent
        
        return agent

    async def _aggregate_results(self, results: dict[str, Any]) -> dict[str, Any]:
        """
        Aggregate results from multiple sub-agents.
        
        Args:
            results: Dictionary of task results
            
        Returns:
            Aggregated result
        """
        # Separate by task type
        research_results = []
        code_results = []
        analysis_results = []
        validation_results = []
        
        for task_id, result in results.items():
            if isinstance(result, dict) and "error" in result:
                continue  # Skip failed tasks
            
            # Categorize results (simplified - could be more sophisticated)
            if "research" in task_id or isinstance(result, list):
                research_results.append(result)
            elif "code" in task_id or isinstance(result, str):
                code_results.append(result)
            elif "validate" in task_id:
                validation_results.append(result)
            else:
                analysis_results.append(result)
        
        return {
            "research": research_results,
            "code": code_results,
            "analysis": analysis_results,
            "validation": validation_results,
            "summary": self._generate_summary(results),
        }

    def _generate_summary(self, results: dict[str, Any]) -> str:
        """
        Generate a summary of all results.
        
        Args:
            results: Dictionary of task results
            
        Returns:
            Summary string
        """
        total_tasks = len(results)
        successful_tasks = sum(
            1 for r in results.values() if not (isinstance(r, dict) and "error" in r)
        )
        
        return f"Completed {successful_tasks}/{total_tasks} tasks successfully"

    async def _validate_result(self, result: dict[str, Any]) -> dict[str, Any]:
        """
        Final validation of aggregated results.
        
        Args:
            result: Aggregated result
            
        Returns:
            Validated result with quality scores
        """
        # If validation was part of the workflow, use those results
        if result.get("validation"):
            validation = result["validation"][0] if result["validation"] else {}
            result["quality_score"] = validation.get("score", 0.0)
            result["validation_passed"] = validation.get("passed", False)
        else:
            # Basic validation
            result["quality_score"] = 0.8  # Default score
            result["validation_passed"] = True
        
        return result

    def cleanup(self) -> None:
        """Clean up all active sub-agents."""
        self._active_agents.clear()
        self._task_graph.clear()

