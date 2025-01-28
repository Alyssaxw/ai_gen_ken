"""
Reviewer Agent Module - Responsible for code review and quality assurance.
"""
from typing import Dict, Any, Tuple
import autogen


class ReviewerAgent:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Reviewer Agent.

        Args:
            config (Dict[str, Any]): Configuration dictionary containing model settings
        """
        self.agent = autogen.AssistantAgent(
            name="reviewer",
            llm_config=config,
            system_message="""You are a code reviewer agent. Your responsibilities include:
            1. Reviewing code for PEP 8 compliance
            2. Checking for best practices
            3. Identifying potential bugs
            4. Ensuring proper documentation
            5. Providing constructive feedback
            
            If the code meets all standards, include 'PASSED: Code meets all standards.'
            in your response. Otherwise, provide specific feedback about what needs to be fixed.
            
            End your response with TERMINATE""",
        )
        self.user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=1,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={"work_dir": "coding", "use_docker": False},
        )

    def review_code(self, code: str) -> Tuple[bool, str]:
        """
        Review the provided code and provide feedback.

        Args:
            code (str): Code to review

        Returns:
            Tuple[bool, str]: (passed_review, feedback)
        """
        print("[Reviewer Agent] Reviewing code...")
        
        # Initialize the chat
        self.user_proxy.initiate_chat(
            self.agent,
            message=f"""Please review the following Python code:
            
            {code}
            
            Provide your review feedback and end with TERMINATE""",
        )
        
        # Extract the last message from the agent which should contain the review
        review = self.user_proxy.chat_messages[self.agent.name][-1]["content"]
        # Remove the TERMINATE string
        review = review.replace("TERMINATE", "").strip()
        
        # Check if code passed review
        passed = "PASSED: Code meets all standards." in review
        
        # If passed, just return that it passed, otherwise return the feedback
        if passed:
            feedback = "Code passed review"
        else:
            feedback = review
            
        return passed, feedback