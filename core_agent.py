import os
from langchain_groq import ChatGroq
from langchain_experimental.agents import create_pandas_dataframe_agent

def create_agent(df, api_key):
    llm = ChatGroq(
        api_key=api_key, 
        model_name="llama-3.1-8b-instant", 
        temperature=0 
    )
    
    agent = create_pandas_dataframe_agent(
        llm, 
        df, 
        verbose=True, 
        allow_dangerous_code=True,
        max_iterations=5,
        handle_parsing_errors=True  
    )
    
    return agent
