import os
import enum
import json
import openai
import dotenv
from pydantic import BaseModel
from typing import List, Dict, Optional
from api.agent.prompt import SYSTEM_PROMPT
from api.agent.zerepy import (
    get_balance,
    transfer_sonic_custom,
    sonic_custom_swap,
)

dotenv.load_dotenv()


class Action(enum.Enum):
    CHAT = "chat"
    SWAP = "swap"
    WITHDRAW = "withdraw"
    BALANCE = "balance"


class BalanceResponse(BaseModel):
    address: str
    asset: str
    action: Action


class WithdrawResponse(BaseModel):
    from_address: Optional[str] = None
    to_address: Optional[str] = None
    amount: Optional[float] = None
    asset: Optional[str] = None
    action: Action


class SwapResponse(BaseModel):
    token_in: Optional[str] = None
    token_out: Optional[str] = None
    amount: Optional[float] = None
    action: Action


class ChatResponse(BaseModel):
    message: str
    action: Action


class AgentResponse(BaseModel):
    success: bool
    action: Action
    data: Optional[WithdrawResponse | SwapResponse | ChatResponse | BalanceResponse] = (
        None
    )
    error: Optional[str] = None


# Process the response based on action type
def process_response(response: AgentResponse, private_key: Optional[str] = None):
    if not response.success:
        return {
            "status": "error",
            "result": response.error,
        }

    match response.action:
        case Action.CHAT:
            chat_data = response.data
            print(f"Chat Response: {chat_data.message}")
            return {
                "status": "success",
                "action": Action.CHAT,
                "result": chat_data.message,
            }

        case Action.BALANCE:
            balance_data = response.data
            res = get_balance(balance_data.address, balance_data.asset)
            print(f"Balance response: {balance_data}")
            return {
                "status": "success",
                "action": Action.BALANCE,
                "result": res["result"],
            }

        case Action.SWAP:
            swap_data = response.data
            print(
                f"Swap: {swap_data.amount} {swap_data.token_in} to {swap_data.token_out}"
            )
            res = sonic_custom_swap(
                token_in=swap_data.token_in,
                token_out=swap_data.token_out,
                amount=str(swap_data.amount),
                private_key=private_key,
            )
            return {
                "status": "success",
                "action": Action.SWAP,
                "result": res["result"],
            }

        case Action.WITHDRAW:
            withdraw_data = response.data
            print(
                f"Withdraw:{withdraw_data.amount} from {withdraw_data.from_address} to {withdraw_data.to_address}"
            )
            res = transfer_sonic_custom(
                to_address=withdraw_data.to_address,
                amount=str(withdraw_data.amount),
                private_key=private_key,
                token_address=withdraw_data.asset,
            )
            return {
                "status": "success",
                "action": Action.WITHDRAW,
                "result": res["result"],
            }

        case _:
            print(f"Unknown action: {response.action}")


class Agent:
    def __init__(self, model: str):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def structured_call(
        self, system_prompt: str, messages: List[Dict[str, str]]
    ) -> AgentResponse:
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                *messages,
            ],
            temperature=0.7,
            response_format=AgentResponse,
        )
        return response.choices[0].message.parsed


if __name__ == "__main__":
    agent = Agent(model=os.getenv("OPENAI_MODEL"), system_prompt=SYSTEM_PROMPT)
    response = agent.structured_call(
        system_prompt=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": """
                   helper informations:
                   user address is: 0x7EC6e6E82834754762E244A349fea27C51eB84b6
                   user wont be providing address, use the address above, user provides only token address
                   if user wants sonic or native asset, or doesnt specify asset address, default to 0xnative
                   --------------------------------------------------------
                   i want to transfer 0.001 sonic to 0x0000000000000000000000000000000000000000
                   """,
                #    i want to check my balances for token 0x29219dd400f2Bf60E5a23d13Be72B486D4038894
            }
        ],
    )
    print(response)

    # Process the example response
    res = process_response(response, private_key=os.getenv("TEST_PRIVATE_KEY"))
    print("res status", res["status"])
    print("res result", res["result"])
