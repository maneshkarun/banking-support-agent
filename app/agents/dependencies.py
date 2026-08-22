from typing import Any

from fastapi import Request


def get_banking_agent(request: Request) -> Any:
    return request.app.state.banking_agent