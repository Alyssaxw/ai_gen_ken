"""
QA Agent Module - Responsible for testing and validation.
"""
from typing import Dict, Any, Tuple
import autogen


class QAAgent:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the QA Agent.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing model settings
        """
        self.agent = autogen.AssistantAgent(
            name="qa",
            llm_config=config,
            system_message="""You are a QA testing agent. Your responsibilities include:
            1. Writing and executing test cases
            2. Validating functionality
            3. Ensuring edge cases are covered
            4. Reporting test results
            5. Identifying potential issues
            
            Write and execute test cases for the given code. Include edge cases.
            If all tests pass, include 'PASSED: All tests successful.'
            Otherwise, provide details about failed tests.
            
            End your response with TERMINATE""",
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "coding", "use_docker": False},
        )

    def run_tests(self, code: str) -> Tuple[bool, str]:
        """
        Test the provided code implementation.

        Args:
            code (str): Code to test

        Returns:
            Tuple[bool, str]: (tests_passed, test_results)
        """
        print("[QA Agent] Running tests...")
        
        # Initialize the chat
        self.user_proxy.initiate_chat(
            self.agent,
            message=f"""Please test the following Python code. Write test cases including edge cases,
            execute them, and provide the results:
            
            {code}
            
            After running the tests, provide a summary and end with TERMINATE""",
        )
        
        # Extract the last message from the agent which should contain the test results
        results = self.user_proxy.chat_messages[self.agent.name][-1]["content"]
        # Remove the TERMINATE string
        results = results.replace("TERMINATE", "").strip()
        
        # Check if all tests passed
        passed = "PASSED: All tests successful." in results
        
        return passed, results