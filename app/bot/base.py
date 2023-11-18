"""Agent for working with pandas objects."""
from typing import Any, Dict, List, Optional

from langchain.agents.agent import AgentExecutor
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.llms.base import BaseLLM

from .prompt import PREFIX, SUFFIX


from .tools.python.tool import PythonAstREPLTool
from .tools.Transaction.tool import TransactionTool
from .tools.Balances.tool import BalanceTool
from .tools.TokenPrices.tool import TokenPricesTool
from .tools.PortfolioBuilder.tool import PortfolioBuilderTool

from .helpers.historic_data_local import load_and_organize_data


from .ZeroShotAgent.base import ZeroShotAgent

import openai
from os import environ
openai.api_key = environ["OPENAI_API_KEY"]




def create_agent(
    llm: BaseLLM,
    callback_manager: Optional[BaseCallbackManager] = None,
    prefix: str = PREFIX,
    suffix: str = SUFFIX,
    input_variables: Optional[List[str]] = None,
    verbose: bool = True,
    return_intermediate_steps: bool = False,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    query: Optional[Any] = None,
    **kwargs: Any,
) -> AgentExecutor:
    """Construct a crypto agent."""
    
    input_variables = ["input", "agent_scratchpad"]



    token_data_df = load_and_organize_data("historical_data.json")
    
    
    input_variables = ["token_data_df"] + \
        ["input", "agent_scratchpad"]
        
    python_variables = {
        "token_data_df": token_data_df,
    }
    
    tools = [TransactionTool(), BalanceTool(), TokenPricesTool(), PythonAstREPLTool(locals=python_variables),PortfolioBuilderTool()]#, 


    prompt = ZeroShotAgent.create_prompt(
        tools, prefix=prefix, suffix=suffix, input_variables=input_variables
    )


    structure = str(token_data_df.head())
    
    partial_prompt = prompt.partial(token_data_df=structure)

    
    llm_chain = LLMChain(
        llm=llm,
        prompt=partial_prompt,
        callback_manager=callback_manager,
    )

    tool_names = [tool.name for tool in tools]

    agent = ZeroShotAgent(
        llm_chain=llm_chain,
        allowed_tools=tool_names,
        callback_manager=callback_manager,
        **kwargs,
    )

    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        callback_manager=callback_manager,
        verbose=verbose,
        return_intermediate_steps=return_intermediate_steps,
        max_iterations=max_iterations,
        max_execution_time=max_execution_time,
        early_stopping_method=early_stopping_method,
        handle_parsing_errors=True,
        **(agent_executor_kwargs or {}),
    )


