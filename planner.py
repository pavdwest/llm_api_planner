import yaml

from langchain.requests import RequestsWrapper
from langchain.agents.agent_toolkits.openapi.spec import reduce_openapi_spec
from langchain.llms.openai import OpenAI
from langchain.agents.agent_toolkits.openapi import planner

import config


# LLM
llm = OpenAI(temperature=0.0, openai_api_key=config.OPENAI_API_KEY)

# API Agent
with open('api_spec.json') as f:
    raw_api_spec = yaml.load(f, Loader=yaml.Loader)

api_spec = reduce_openapi_spec(raw_api_spec)

requests_wrapper = RequestsWrapper()
api_agent = planner.create_openapi_agent(api_spec, requests_wrapper, llm)

query = (
    # 'The South African Rand weakened significantly last night. Get me a list of my portfolios that would be affected and show me their worst performing instruments.'
    # "Get all my portfolios that have a currency of 'ZAR' and get their worst performing holding. Include the instrument and the portfolio names in the response."
    "Get me the names of the two worst performing instruments in each of my portfolios with a currency of 'ZAR'."
    # "Get all my portfolios with currency of 'ZAR' and show me their worst performing holding. Provide all the details of the holding including the portfolio and the instrument."
    # "Get all my portfolios with currency of 'South African Rand' and show me their worst performing holding."

)

api_agent.run(query)
