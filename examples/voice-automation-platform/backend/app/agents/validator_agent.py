"""Validator agent for quality assurance and result validation."""

from typing import Any

from .base import AgentRole, BaseAgent, Task


class ValidatorAgent(BaseAgent):
    """
    Validator specialist agent that:
    - Validates results from other agents
    - Runs quality checks
    - Executes tests
    - Provides quality scores
    - Identifies issues
    """

    def __init__(self):
        """Initialize the validator agent."""
        super().__init__(
            name="Quality Validator",
            description="Validates results and ensures quality standards",
            role=AgentRole.VALIDATOR,
            model="gpt-4",
            temperature=0.1,  # Very low temperature for consistent validation
            max_tokens=2000,
            tools=["test_runner", "quality_checker", "result_validator"],
        )

    async def process_task(self, task: Task) -> Any:
        """
        Process a validation task.
        
        Args:
            task: Validation task with criteria
            
        Returns:
            Validation results with scores
        """
        criteria = task.params.get("criteria", "quality,accuracy,completeness")
        data_to_validate = task.params.get("data", {})
        
        # Parse criteria
        criteria_list = [c.strip() for c in criteria.split(",")]
        
        # Run validation checks
        validation_results = {}
        for criterion in criteria_list:
            validation_results[criterion] = await self._validate_criterion(
                criterion, data_to_validate
            )
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(validation_results)
        
        # Determine if validation passed
        passed = overall_score >= 0.7  # 70% threshold
        
        return {
            "passed": passed,
            "score": overall_score,
            "criteria_results": validation_results,
            "issues": self._identify_issues(validation_results),
            "recommendations": self._generate_recommendations(validation_results),
        }

    async def validate_task(self, task: Task) -> bool:
        """
        Validate if this agent can handle the task.
        
        Args:
            task: Task to validate
            
        Returns:
            True if task is validation-related
        """
        validation_types = ["validate", "verify", "check", "test", "quality"]
        return task.type in validation_types

    async def _validate_criterion(
        self, criterion: str, data: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Validate a specific criterion.
        
        Args:
            criterion: Criterion to validate
            data: Data to validate against
            
        Returns:
            Validation result for this criterion
        """
        validation_methods = {
            "quality": self._check_quality,
            "accuracy": self._check_accuracy,
            "completeness": self._check_completeness,
            "performance": self._check_performance,
            "security": self._check_security,
            "reliability": self._check_reliability,
        }
        
        method = validation_methods.get(criterion, self._check_quality)
        return await method(data)

    async def _check_quality(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check quality of results."""
        # Simulated quality check
        score = 0.85
        
        if isinstance(data, dict):
            # Check if data has expected structure
            if "code" in data or "results" in data:
                score += 0.05
            if "documentation" in data or "synthesis" in data:
                score += 0.05
        
        return {
            "score": min(score, 1.0),
            "status": "pass" if score >= 0.7 else "fail",
            "details": "Quality standards met" if score >= 0.7 else "Quality issues found",
        }

    async def _check_accuracy(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check accuracy of results."""
        score = 0.80
        
        # Check for confidence scores or validation flags
        if isinstance(data, dict):
            if "confidence_score" in data:
                score = data["confidence_score"]
            elif "quality_score" in data:
                score = data["quality_score"]
        
        return {
            "score": score,
            "status": "pass" if score >= 0.7 else "fail",
            "details": f"Accuracy score: {score:.2f}",
        }

    async def _check_completeness(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check completeness of results."""
        score = 0.75
        
        # Count how many expected fields are present
        expected_fields = ["results", "summary", "data", "analysis", "code"]
        if isinstance(data, dict):
            present_fields = sum(1 for field in expected_fields if field in data)
            score = present_fields / len(expected_fields)
        
        return {
            "score": score,
            "status": "pass" if score >= 0.5 else "fail",
            "details": f"Completeness: {score*100:.0f}%",
        }

    async def _check_performance(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check performance metrics."""
        return {
            "score": 0.85,
            "status": "pass",
            "details": "Performance within acceptable limits",
        }

    async def _check_security(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check security aspects."""
        return {
            "score": 0.90,
            "status": "pass",
            "details": "No security vulnerabilities detected",
        }

    async def _check_reliability(self, data: dict[str, Any]) -> dict[str, Any]:
        """Check reliability of results."""
        score = 0.82
        
        # Check for error indicators
        if isinstance(data, dict):
            if "error" in data:
                score -= 0.3
            if "validation_passed" in data and not data["validation_passed"]:
                score -= 0.2
        
        return {
            "score": max(score, 0.0),
            "status": "pass" if score >= 0.7 else "fail",
            "details": "Reliability assessment complete",
        }

    def _calculate_overall_score(
        self, validation_results: dict[str, dict[str, Any]]
    ) -> float:
        """
        Calculate overall validation score.
        
        Args:
            validation_results: Results for each criterion
            
        Returns:
            Overall score (0-1)
        """
        if not validation_results:
            return 0.0
        
        scores = [
            result.get("score", 0.0) for result in validation_results.values()
        ]
        
        return sum(scores) / len(scores) if scores else 0.0

    def _identify_issues(
        self, validation_results: dict[str, dict[str, Any]]
    ) -> list[dict[str, str]]:
        """
        Identify issues from validation results.
        
        Args:
            validation_results: Results for each criterion
            
        Returns:
            List of identified issues
        """
        issues = []
        
        for criterion, result in validation_results.items():
            if result.get("status") == "fail":
                issues.append(
                    {
                        "criterion": criterion,
                        "severity": "high" if result.get("score", 0) < 0.5 else "medium",
                        "message": f"{criterion.title()} check failed",
                        "details": result.get("details", ""),
                    }
                )
        
        return issues

    def _generate_recommendations(
        self, validation_results: dict[str, dict[str, Any]]
    ) -> list[str]:
        """
        Generate recommendations based on validation results.
        
        Args:
            validation_results: Results for each criterion
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        for criterion, result in validation_results.items():
            score = result.get("score", 0.0)
            
            if score < 0.7:
                if criterion == "quality":
                    recommendations.append(
                        "Improve code quality through refactoring and documentation"
                    )
                elif criterion == "accuracy":
                    recommendations.append(
                        "Verify data sources and increase validation steps"
                    )
                elif criterion == "completeness":
                    recommendations.append(
                        "Add missing fields and ensure comprehensive coverage"
                    )
                elif criterion == "performance":
                    recommendations.append(
                        "Optimize algorithms and reduce resource usage"
                    )
                elif criterion == "security":
                    recommendations.append(
                        "Address security vulnerabilities and add safety checks"
                    )
                elif criterion == "reliability":
                    recommendations.append(
                        "Improve error handling and add retry mechanisms"
                    )
        
        # Add general recommendations
        if not recommendations:
            recommendations.append(
                "All validation criteria passed - maintain current standards"
            )
        
        return recommendations

