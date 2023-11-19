"""A tool for running python code in a REPL."""

import ast
import asyncio
import re
import sys
from contextlib import redirect_stdout
from io import StringIO
from typing import Any, Dict, Optional, Type
import json

from os import environ
import time
from datetime import datetime, timedelta


from time import sleep
import requests
from web3 import Web3



from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel, Field, root_validator
from langchain.tools.base import BaseTool

from dotenv import load_dotenv


from ...helpers.oneinch import fetch_token_data, generateCallDataForApprove,generateCallDataForSwap
load_dotenv('../../../.env')


def clean_json(json_input):
    try:
        # Check if input is already a dictionary
        if isinstance(json_input, dict):
            return json_input
        # Remove leading/trailing white spaces
        json_string = json_input.strip()
        # Parse JSON string to dictionary
        print(json_string)
        json_dict = json.loads(json_string)
        return json_dict
    except json.JSONDecodeError:
        return "Invalid JSON"
    
    
class TransactionToolInputs(BaseModel):
    query: str = Field(
        description="this should be a valid json which contains a key value for from_token_name, to_token_name, amount, chain_name")


class TransactionTool(BaseTool):
    """A tool for generating syntetic data with an external api."""

    name: str = "transaction"
    description: str = (
        "This tool enables the ai agent to make transactions on a blockchain. This makes transactions on the base blockchain."
        "To use this tool: You should pass in a valid json which contains a key value for from_token_name, to_token_name, amount, chain_name."
        "When you pass the json in, make sure its a string. Do not include ```json```"
        "Use this tool to make transactions."
        "You do not need to check current prices in order to do a swap. Just do this tool first if the user mentions a swap."
        "You must return JSON and this JSON must go to the user directly."
    )
    globals: Optional[Dict] = Field(default_factory=dict)
    locals: Optional[Dict] = Field(default_factory=dict)
    sanitize_input: bool = True
    args_schema: Type[BaseModel] = TransactionToolInputs

    @root_validator(pre=True)
    def validate_python_version(cls, values: Dict) -> Dict:
        """Validate valid python version."""
        if sys.version_info < (3, 9):
            raise ValueError(
                "This tool relies on Python 3.9 or higher "
                "(as it uses new functionality in the `ast` module, "
                f"you have Python version: {sys.version}"
            )
        return values

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        try:
            print("RUNNING THE TRANSACTION TOOOL!!!!!")
            
            query=clean_json(query)
            
            wallet_address = "0x8cF84867ba54bd078F678fb276BB1a103efce7d3"
            print(query)
            
            
            print("from_token_address",query['from_token_name'])
            print("to_token_address", query['to_token_name'])
            print("amount", query['amount'])
            
            
            from_token_info = fetch_token_data(query['from_token_name'], 1)
            sleep(1)
            print(from_token_info)
            to_token_info = fetch_token_data(query['to_token_name'], 1)
            print(to_token_info)
            
            from_token_address = from_token_info['address']
            to_token_address = to_token_info['address']
            
            print("from_address",from_token_address)
            print("to_address",to_token_address )
            
            edited_amount_with_decimals = query['amount'] * 10 ** from_token_info['decimals']
        
            print("amount", edited_amount_with_decimals)
            sleep(1)
            print("generating the calldata for the approval")
            calldata_approve = generateCallDataForApprove(from_token_address,edited_amount_with_decimals)
            print(calldata_approve)
            
            print("===========================================")
            sleep(1)
            calldata_swap = generateCallDataForSwap(from_token_address,to_token_address, edited_amount_with_decimals, wallet_address)
            print(calldata_swap)
            
            
            RETURN_OBJECT = {
                "from_name": from_token_info['symbol'],
                "to_name": to_token_info['symbol'],
                "from_amount": query['amount']
            }
            
            return RETURN_OBJECT

        except Exception as e:
            return "{}: {}".format(type(e).__name__, str(e))

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool asynchronously."""

        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self._run, query)

        return result



    def test():
        print("yeah")
        # generateCallDataForSwap(from_address,to_address, amount, wallet_address)
        # generateCallDataForSwap()