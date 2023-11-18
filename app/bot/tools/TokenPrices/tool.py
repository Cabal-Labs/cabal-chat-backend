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


from ...helpers.oneinch import get_prices_for_addresses
load_dotenv('../../../.env')



def clean_json(json_input):
    try:
        # Check if input is already a dictionary
        if isinstance(json_input, dict):
            return json_input
        # Remove leading/trailing white spaces
        json_string = json_input.strip()
        # Parse JSON string to dictionary
        json_dict = json.loads(json_string)
        return json_dict
    except json.JSONDecodeError:
        return "Invalid JSON"
    
    
class TransactionToolInputs(BaseModel):
    query: str = Field(
        description="this should be a valid json which contains a key value for from_token_name, to_token_name, amount, chain_name")


class TokenPricesTool(BaseTool):
    """A tool for generating syntetic data with an external api."""

    name: str = "token_price"
    description: str = (
        "This tool enables you to enter in a token address and be able to get the token's price from it. This is the current live prive of the token"
        "To use this tool: You should pass in a valid json which contains a key value for 'token_addresses' (which is an array of token addresses), 'chain_name' if none are specified, assume ethereum."
        "When you pass the json in, make sure its a string. Do not include ```json```"
        "If you do not have the token_address, you need to get that first. "
        "When giving your response, if the token is USDC, DIA, USDT the user knows that these are stablecoins and thus you do not need to describe how much the stablecoin costs."
      
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
            print("RUNNING THE TOKEN PRICE TOOOL!!!!!")
            
            query=clean_json(query)
            
            print(query)
            wallet_address = "0x8cF84867ba54bd078F678fb276BB1a103efce7d3"
       
    
            response = get_prices_for_addresses(query['token_addresses'],1)
            
            print(response)
            
            return response

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
        print("testing")
        a = get_prices_for_addresses(["0x1707a9bad232d728afded75faced38ec90eaa41e"])
        
        
        print(a)
        # generateCallDataForSwap(from_address,to_address, amount, wallet_address)
        # generateCallDataForSwap()