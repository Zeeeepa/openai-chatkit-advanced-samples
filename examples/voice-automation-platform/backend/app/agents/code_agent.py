"""Code agent for code generation, analysis, and testing."""

from typing import Any

from .base import AgentRole, BaseAgent, Task


class CodeAgent(BaseAgent):
    """
    Code specialist agent that:
    - Generates code based on requirements
    - Analyzes existing code
    - Creates test cases
    - Performs code reviews
    - Suggests improvements
    """

    def __init__(self):
        """Initialize the code agent."""
        super().__init__(
            name="Code Specialist",
            description="Generates, analyzes, and improves code",
            role=AgentRole.CODE,
            model="gpt-4",
            temperature=0.2,  # Lower temperature for more consistent code
            max_tokens=4000,
            tools=["code_generator", "code_analyzer", "test_runner", "cli_executor"],
        )

    async def process_task(self, task: Task) -> Any:
        """
        Process a code-related task.
        
        Args:
            task: Code task with requirements
            
        Returns:
            Generated/analyzed code with tests
        """
        requirements = task.params.get("requirements", task.description)
        task_type = task.params.get("task_type", "generate")
        
        if task_type == "generate":
            return await self._generate_code(requirements)
        elif task_type == "analyze":
            return await self._analyze_code(requirements)
        elif task_type == "test":
            return await self._generate_tests(requirements)
        elif task_type == "review":
            return await self._review_code(requirements)
        else:
            return await self._generate_code(requirements)

    async def validate_task(self, task: Task) -> bool:
        """
        Validate if this agent can handle the task.
        
        Args:
            task: Task to validate
            
        Returns:
            True if task is code-related
        """
        code_types = ["code", "implement", "build", "create", "develop"]
        return task.type in code_types

    async def _generate_code(self, requirements: str) -> dict[str, Any]:
        """
        Generate code from requirements.
        
        Args:
            requirements: Code requirements
            
        Returns:
            Generated code with documentation
        """
        # Simulated code generation
        # In real implementation: await self.call_tool("code_generator", prompt=requirements)
        
        code = f'''"""
Generated code for: {requirements}
"""

from typing import Any


class GeneratedClass:
    """Auto-generated class based on requirements."""
    
    def __init__(self):
        """Initialize the class."""
        self.data = {{}}
    
    def process(self, input_data: Any) -> Any:
        """
        Process input data according to requirements.
        
        Args:
            input_data: Input to process
            
        Returns:
            Processed result
        """
        # Implementation based on: {requirements}
        return {{"status": "processed", "data": input_data}}
    
    def validate(self) -> bool:
        """Validate the current state."""
        return True
'''
        
        return {
            "code": code,
            "language": "python",
            "framework": "standard",
            "quality_score": 0.85,
            "documentation": "Auto-generated with docstrings",
            "test_coverage": 0.0,  # No tests yet
            "recommendations": [
                "Add error handling",
                "Implement input validation",
                "Add logging",
                "Create comprehensive tests",
            ],
        }

    async def _analyze_code(self, code: str) -> dict[str, Any]:
        """
        Analyze existing code.
        
        Args:
            code: Code to analyze
            
        Returns:
            Analysis results
        """
        return {
            "complexity": "medium",
            "maintainability_score": 0.75,
            "issues_found": [
                {"type": "style", "message": "Missing type hints", "line": 10},
                {"type": "performance", "message": "Could optimize loop", "line": 25},
            ],
            "suggestions": [
                "Add more documentation",
                "Consider using list comprehension",
                "Extract magic numbers to constants",
            ],
            "metrics": {
                "lines_of_code": 100,
                "cyclomatic_complexity": 5,
                "comment_ratio": 0.15,
            },
        }

    async def _generate_tests(self, code: str) -> dict[str, Any]:
        """
        Generate test cases for code.
        
        Args:
            code: Code to test
            
        Returns:
            Test cases
        """
        test_code = f'''"""
Test cases for generated code.
"""

import pytest
from typing import Any


class TestGeneratedClass:
    """Test suite for GeneratedClass."""
    
    def test_initialization(self):
        """Test class initialization."""
        obj = GeneratedClass()
        assert obj.data == {{}}
    
    def test_process_valid_input(self):
        """Test process with valid input."""
        obj = GeneratedClass()
        result = obj.process({{"key": "value"}})
        assert result["status"] == "processed"
        assert result["data"] == {{"key": "value"}}
    
    def test_process_empty_input(self):
        """Test process with empty input."""
        obj = GeneratedClass()
        result = obj.process({{}})
        assert result["status"] == "processed"
    
    def test_validate(self):
        """Test validation method."""
        obj = GeneratedClass()
        assert obj.validate() is True
    
    @pytest.mark.parametrize("input_data,expected", [
        ({{"a": 1}}, {{"status": "processed", "data": {{"a": 1}}}}),
        ({{"b": 2}}, {{"status": "processed", "data": {{"b": 2}}}}),
    ])
    def test_process_parametrized(self, input_data, expected):
        """Test process with various inputs."""
        obj = GeneratedClass()
        result = obj.process(input_data)
        assert result == expected
'''
        
        return {
            "test_code": test_code,
            "test_framework": "pytest",
            "test_count": 5,
            "coverage_estimate": 0.80,
            "test_types": ["unit", "parametrized"],
            "run_instructions": "pytest test_generated.py -v",
        }

    async def _review_code(self, code: str) -> dict[str, Any]:
        """
        Perform code review.
        
        Args:
            code: Code to review
            
        Returns:
            Review results
        """
        return {
            "overall_score": 0.80,
            "categories": {
                "readability": 0.85,
                "maintainability": 0.75,
                "performance": 0.80,
                "security": 0.90,
                "testing": 0.60,
            },
            "positive_points": [
                "Clear function names",
                "Good documentation",
                "Proper type hints",
            ],
            "issues": [
                {
                    "severity": "medium",
                    "category": "testing",
                    "message": "Test coverage below 80%",
                    "recommendation": "Add more edge case tests",
                },
                {
                    "severity": "low",
                    "category": "style",
                    "message": "Some long functions",
                    "recommendation": "Consider breaking into smaller functions",
                },
            ],
            "action_items": [
                "Increase test coverage",
                "Add error handling",
                "Document edge cases",
            ],
        }

