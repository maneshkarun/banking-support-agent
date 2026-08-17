"""Command-line entry point for the banking assistant."""

from typing import Any

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from app.tools.banking_tools import (
    get_account_balance,
    get_complete_account_details,
    get_customer_details,
)


def build_agent() -> Any:
    """Build and return the banking agent with its read-only tools."""

    llm = ChatOpenAI(
        model="models/gemma-4-12b-it-Q8_0.gguf",
        base_url="http://localhost:8080/v1",
        api_key="local-development-key",
    )
    return create_agent(
        model=llm,
        tools=[get_account_balance, get_complete_account_details, get_customer_details],
        system_prompt="You are a helpful banking assistant.",
    )


def main() -> None:
    """Run one example request against the locally hosted model."""

    agent = build_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "what is account balance of customer id 1"}]}
    )
    print(result["messages"])


if __name__ == "__main__":
    main()
