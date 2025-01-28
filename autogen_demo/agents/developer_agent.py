"""
Developer Agent Module - Responsible for code generation and implementation.
"""
from typing import Dict, Any
import autogen


class DeveloperAgent:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Developer Agent.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing model settings
        """
        self.agent = autogen.AssistantAgent(
            name="developer",
            llm_config=config,
            system_message="""You are a Python developer agent. Your responsibilities include:
            1. Writing clean, efficient, and well-documented Python code
            2. Following PEP 8 standards
            3. Implementing requested functionality
            4. Addressing review feedback
            5. Using type hints and docstrings
            
            When writing code:
            - Only provide the code, no explanations
            - Ensure proper error handling
            - Include type hints and docstrings
            - Follow PEP 8 standards
            """,
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            code_execution_config=False,  # Disable code execution
        )

    def generate_code(self, task_description: str) -> str:
        """
        Generate code based on the given task description.

        Args:
            task_description (str): Description of the coding task

        Returns:
            str: Generated code
        """
        print("[Developer Agent] Generating code...")
        
        # Initialize the chat
        self.user_proxy.initiate_chat(
            self.agent,
            message=f"""Write Python code for the following task. Only provide the code, no explanations:
            {task_description}""",
        )
        
        # Get the last message from the conversation
        messages = self.user_proxy.chat_messages.get(self.agent.name, [])
        if not messages:
            return "Error: No response from agent"
            
        # Extract code from the message
        response = messages[-1]["content"]
        
        # Clean up the response to extract just the code
        if "```python" in response:
            code = response.split("```python")[1].split("```")[0].strip()
        else:
            code = response.strip()
            
        return code

    def modify_code(self, code: str, feedback: str) -> str:
        """
        Modify code based on reviewer feedback.

        Args:
            code (str): Original code
            feedback (str): Feedback from the reviewer

        Returns:
            str: Modified code
        """
        print("[Developer Agent] Modifying code based on feedback...")
        
        # Initialize the chat
        self.user_proxy.initiate_chat(
            self.agent,
            message=f"""Modify this code based on the feedback. Only provide the modified code, no explanations:

            Original code:
            {code}
            
            Feedback:
            {feedback}""",
        )
        
        # Get the last message from the conversation
        messages = self.user_proxy.chat_messages.get(self.agent.name, [])
        if not messages:
            return "Error: No response from agent"
            
        # Extract code from the message
        response = messages[-1]["content"]
        
        # Clean up the response to extract just the code
        if "```python" in response:
            code = response.split("```python")[1].split("```")[0].strip()
        else:
            code = response.strip()
            
        return code