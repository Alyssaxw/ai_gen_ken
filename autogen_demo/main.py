"""
Main module for orchestrating the AutoGen demo with multiple agents.
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv
from agents import DeveloperAgent, ReviewerAgent, QAAgent

def load_config() -> Dict[str, Any]:
    """
    Load configuration including API keys and model settings.

    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    load_dotenv()
    
    return {
        "config_list": [{
            "model": os.getenv("MODEL_NAME", "openai/gpt-4"),
            "base_url": os.getenv("API_BASE", "https://openrouter.ai/api/v1"),
            "api_key": os.getenv("OPENROUTER_API_KEY"),
        }],
        "temperature": 0.1,
    }

def main():
    """
    Main function to orchestrate the interaction between agents.
    """
    # Load configuration
    config = load_config()
    
    # Initialize agents
    developer = DeveloperAgent(config)
    reviewer = ReviewerAgent(config)
    qa = QAAgent(config)
    
    # Example task
    task = """
    Create a function that calculates the factorial of a number recursively.
    Include proper error handling and type hints.
    """
    
    # Development cycle
    print("\n=== Starting Development Cycle ===\n")
    
    # Step 1: Generate code
    code = developer.generate_code(task)
    print("\n=== Generated Code ===\n")
    print(code)
    
    # Step 2: Review code
    passed_review, feedback = reviewer.review_code(code)
    print("\n=== Code Review Results ===\n")
    if not passed_review:
        print("Review feedback:", feedback)
        # Modify code based on feedback
        code = developer.modify_code(code, feedback)
        print("\n=== Modified Code ===\n")
        print(code)
    
    # Step 3: QA Testing
    tests_passed, test_results = qa.run_tests(code)
    print("\n=== QA Test Results ===\n")
    print(test_results)
    
    if tests_passed:
        print("\n=== Development Cycle Completed Successfully ===\n")
    else:
        print("\n=== Development Cycle Completed with Issues ===\n")

if __name__ == "__main__":
    main()