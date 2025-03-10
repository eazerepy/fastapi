import enum
import time
from typing import Optional
from api.agent.zerepy_client import ZerePyClient

from dotenv import load_dotenv
import os

# Load environment variables from .env.test
load_dotenv(".env")


class TransferActions(enum.Enum):
    WITHDRAW = "withdraw"
    SWEEP = "sweep"
    SWAP = "swap"
    CHAT = "chat"


BURN_ADDRESS = 0x0000000000000000000000000000000000000001
USDC_ADDRESS = 0x1C7D4B196CB0C7B01D743FBC6116A902379C7238
AMOUNT = 0.0001
EVM_PRIVATE_KEY = os.getenv("TEST_PRIVATE_KEY")
AFTER_BROADCAST = 15


client = ZerePyClient("http://localhost:8000")


def get_address():
    res = client.perform_action(
        connection="evm",
        action="get-address",
    )
    print(res)
    return res


def get_balance(address: str, token_address: Optional[str] = None):
    print("get_balance", token_address)
    res = client.perform_action(
        connection="sonic",
        action="get-balance",
        params=[address, token_address],
    )
    print(res)
    return res


def transfer_custom(
    to_address: str, amount: str, private_key: str, token_address: Optional[str] = None
):
    res = client.perform_action(
        connection="evm",
        action="transfer-custom",
        params=[to_address, amount, private_key, token_address],
    )
    print(res)
    return res


def transfer_sonic_custom(
    to_address: str, amount: str, private_key: str, token_address: Optional[str] = None
):
    res = client.perform_action(
        connection="sonic",
        action="custom-transfer",
        params=[to_address, amount, private_key, token_address],
    )
    print(res)
    return res


def sonic_custom_swap(
    token_in: str,
    token_out: str,
    amount: str,
    private_key: str,
    slippage: str = "0.5",
):
    print("sonic_custom_swap", token_in, token_out, amount, private_key, slippage)
    res = client.perform_action(
        connection="sonic",
        action="custom-swap",
        params=[token_in, token_out, amount, private_key, slippage],
    )
    print(res)
    return res


client.load_agent("etheth")


if __name__ == "__main__":
    print("transfer-custom")
    res = client.perform_action(
        connection="evm",
        action="transfer-custom",
        params=[
            BURN_ADDRESS,
            AMOUNT,
            EVM_PRIVATE_KEY,
            USDC_ADDRESS,
        ],
    )
    print(res)
    time.sleep(AFTER_BROADCAST)
    get_balance(USDC_ADDRESS)
