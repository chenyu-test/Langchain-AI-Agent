import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import AgentExecutor, create_tool_calling_agent, tool
from pinecone import Pinecone
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.tools import tool
from langchain.agents import ZeroShotAgent
from langchain.memory import ConversationBufferWindowMemory


# Set enviroment variables
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGSMITH_PROJECT"] = "pr-spotless-advertising-76"
os.environ["LANGSMITH_API_KEY"] = st.secrets["LANGSMITH_API_KEY"]
os.environ["TAVILY_API_KEY"] = st.secrets["TAVILY_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
pinecone_api_key = os.environ.get("PINECONE_API_KEY")



model = ChatOpenAI(model="gpt-4o-mini")
search = TavilySearch(max_results=2,
                       description=
        "Verwende das Tool um allgemeine Informationen aus dem Internet zu suchen."
)
tools = [search]
pc = Pinecone(api_key=pinecone_api_key)

# Setup Pinecone Index
from pinecone import ServerlessSpec
index_name = "langchain"
index = pc.Index(index_name)
# index.delete_namespace(namespace="__default__")

#Setup embedding
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")



#Setup vector_store
vector_store = PineconeVectorStore(index=index, embedding=embeddings)

#Short-term memory 
short_term_memory = ConversationBufferWindowMemory(
memory_key="chat_history",
k=3,
return_messages = True
)



# Create a prompt template for the retrieval chain
retrieval_prompt = ChatPromptTemplate.from_template(
    ("""You are a helpful assistant. Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}

    Antwort:
    """
    )
)

#Create document chain
document_chain = create_stuff_documents_chain(model, retrieval_prompt)
retriever = vector_store.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)


#Create Retrieval Tool
@tool
def retrieve_document(query:str) -> str:
  """Verwende das Tool, um relevante Informationen zur KFZ Versicherung der BGV Versicherung zu suchen"""
  result = retrieval_chain.invoke({"input": query})
  return result["answer"]
tools.append(retrieve_document)

# # Create a prompt template for the agent
# agent_prompt = ChatPromptTemplate.from_template(
#     ("""You are a helpful assistant. Answer the following question:

#     Question: {input}

#     {agent_scratchpad}

#     """
#     )
# )

prompt= ZeroShotAgent.create_prompt(
    tools,
    prefix= """You are a helpful chatbot. Only speak in german""",
    suffix= """#Current Coversation:
    {chat_history}
    
    {input}
    
    {agent_scratchpad}""",
    input_variables= ["input", "chat_history", "agent_scratchpad"]
)
#Create Agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(
   agent=agent, 
   tools=tools, 
   memory=short_term_memory,
   verbose=True)
#verbose=True if Chain of Thought should be displayed

def get_response(input):
    result = agent_executor.invoke({
        "input": input
    })
    
    if "Final Answer:" in result['output']:
        think_content=result['output'].split('Final Answer:')[0]
        answer_content=result['output'].split('Final Answer:')[1]
    else:
        think_content =None
        answer_content=None

    return think_content, answer_content, result
    