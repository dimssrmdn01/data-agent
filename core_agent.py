import os
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# =====================================================================
# JURUS SAKTI: PATCH ANTI-CRASH GROQ
# =====================================================================
class SafeChatGroq(ChatGroq):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        response = super()._generate(messages, stop, run_manager, **kwargs)
        for generation in response.generations:
            if generation.message.content is None:
                generation.message.content = ""
        return response

def create_agent(df, api_key):
    os.environ["GROQ_API_KEY"] = api_key
    llm = SafeChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        agent_type="tool-calling",
        allow_dangerous_code=True
    )
    return agent