# AutoGen Demo Project

This project demonstrates the implementation of a multi-agent system using Microsoft's AutoGen framework. The system consists of three specialized agents working together to develop, review, and test Python code.

## Architecture

### Agents

1. **Developer Agent**
   - Primary code generator
   - Follows Python development standards (PEP 8)
   - Implements requested functionality
   - Handles code modifications based on review feedback

2. **Reviewer Agent**
   - Reviews code for:
     - Code quality
     - Best practices
     - PEP 8 compliance
     - Potential bugs
   - Provides feedback to Developer Agent
   - Prints "Code passed review" when code meets standards

3. **QA Agent**
   - Performs automated testing
   - Validates functionality
   - Reports test results
   - Ensures code meets requirements

### Workflow

1. Developer Agent generates initial code
2. Reviewer Agent analyzes the code
   - If issues found: Returns feedback to Developer
   - If approved: Prints "Code passed review"
3. QA Agent runs tests and validates functionality
4. Process repeats if issues are found

## Setup Instructions

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure OpenRouter API:
   - Sign up at https://openrouter.ai/ if you haven't already
   - Get your API key from the dashboard
   - Copy .env.template to .env:
     ```bash
     cp .env.template .env
     ```
   - Edit .env and add your OpenRouter API key:
     ```
     OPENROUTER_API_KEY=your_api_key_here
     MODEL_NAME=openai/gpt-4  # or any other model supported by OpenRouter
     API_BASE=https://openrouter.ai/api/v1
     ```

## Execution Instructions

1. Run the main script:
   ```bash
   python main.py
   ```

2. Monitor the execution logs:
   - Developer Agent actions and code generation
   - Reviewer Agent feedback
   - QA Agent test results

### Example Output

```
[Developer Agent] Generating code...
[Code]
def calculate_sum(a: int, b: int) -> int:
    """Calculate sum of two integers.
    
    Args:
        a (int): First number
        b (int): Second number
        
    Returns:
        int: Sum of a and b
    """
    return a + b

[Reviewer Agent] Reviewing code...
[Reviewer Agent] Code passed review

[QA Agent] Running tests...
[QA Agent] Test cases:
- Test 1: calculate_sum(2, 3) = 5 ✓
- Test 2: calculate_sum(-1, 1) = 0 ✓
[QA Agent] All tests passed
```

## Project Structure

```
autogen_demo/
├── .env.template
├── .env (created from template)
├── README.md
├── main.py
├── agents/
│   ├── __init__.py
│   ├── developer_agent.py
│   ├── reviewer_agent.py
│   └── qa_agent.py
├── tests/
│   ├── __init__.py
│   └── test_cases.py
└── requirements.txt
```

## Available Models

You can use any model supported by OpenRouter by changing the MODEL_NAME in your .env file. Some popular options include:

- openai/gpt-4
- anthropic/claude-2
- google/palm-2-chat-bison
- meta-llama/llama-2-70b-chat

Check OpenRouter's documentation for the complete list of available models and their capabilities.