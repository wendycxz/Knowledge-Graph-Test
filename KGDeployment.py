import os
from dotenv import load_dotenv
import streamlit as st
from langchain.chains import GraphCypherQAChain
from langchain.chat_models import AzureChatOpenAI
from langchain.graphs import Neo4jGraph

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")

# Neo4j connection details
url = "neo4j+s://39edf771.databases.neo4j.io"
username = "neo4j"
password = "31Nwe5MwJKLGHFCTtkmWQVO7R3DU1fYYvX_D63HZGEM"

# Initialize the Neo4j graph instance
graph = Neo4jGraph(
    url=url,
    username=username,
    password=password
)

# Refresh schema to ensure it's up-to-date
graph.refresh_schema()

# Initialize LLMs with different keys
cypher_llm = AzureChatOpenAI(
    azure_endpoint="https://knowledgegraphopenai.openai.azure.com/",
    openai_api_version="v1",
    deployment_name="knowledgegraphGPT4",
    openai_api_key="720d8a2f0b0b479cbe2fb58d190f02f8",
    openai_api_type="azure",
)

qa_llm = AzureChatOpenAI(
    azure_endpoint="https://knowledgegraphopenai.openai.azure.com/",
    openai_api_version="v1",
    deployment_name="openaiforknowledgegraph",
    openai_api_key="720d8a2f0b0b479cbe2fb58d190f02f8",
    openai_api_type="azure",
)

# Create the Cypher QA chain
cypher_chain = GraphCypherQAChain.from_llm(
    graph=graph,
    cypher_llm=cypher_llm,
    qa_llm=qa_llm,
    validate_cypher=True,  # Validate relationship directions
    verbose=True
)

# Streamlit UI
st.title("Knowledge Graph Chatbot")
st.write("Ask any question about the data in our knowledge graph:")

query = st.text_input("Enter your question:")

if st.button("Ask"):
    if query:
        try:
            # Execute the query using the knowledge graph
            result = cypher_chain.run(query)
            if result:
                st.success("Query successful!")
                st.json(result)  # Display the result as JSON for structured output
            else:
                st.info("No data found for your query.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a question to ask the chatbot.")