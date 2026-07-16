import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

load_dotenv()

# =====================================================================
# PATCH ANTI-CRASH GROQ
# =====================================================================
class SafeChatGroq(ChatGroq):
    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        response = super()._generate(messages, stop, run_manager, **kwargs)
        for generation in response.generations:
            if generation.message.content is None:
                generation.message.content = ""  
        return response
# =====================================================================

st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="centered")
st.title("📊 AI Data Analyst Agent")

with st.sidebar:
    st.header("Konfigurasi")
    groq_api_key = st.text_input("Groq API Key", type="password")
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())
    st.divider()

    query = st.chat_input("Tanya sesuatu tentang data ini...")
    
    if query:
        if not os.environ.get("GROQ_API_KEY"):
            st.error("API Key belum diisi.")
            st.stop()

        with st.chat_message("user", avatar="👤"):
            st.markdown(query)
            
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Memproses..."):
                # GUNAKAN KELAS KUSTOM KITA DI SINI
                llm = SafeChatGroq(model="llama-3.3-70b-versatile", temperature=0)
                
                agent = create_pandas_dataframe_agent(
                    llm,
                    df,
                    verbose=True,
                    agent_type="tool-calling",
                    allow_dangerous_code=True
                )
                
                try:
                    secret_prompt = (
                        "\n\nPENTING: Jika membuat grafik, WAJIB simpan dengan "
                        "plt.savefig('temp_chart.png'). Dilarang menggunakan plt.show()."
                    )
                    
                    result = agent.invoke({"input": query + secret_prompt})
                    st.markdown(result["output"])
                    
                    if os.path.exists("temp_chart.png"):
                        st.image("temp_chart.png")
                        os.remove("temp_chart.png")
                        
                except Exception as e:
                    st.error(f"Error: {e}")