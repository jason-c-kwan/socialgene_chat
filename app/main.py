import streamlit as st
from models.neo4j_model import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

import streamlit as st
from models.neo4j_model import Neo4jConnector  # Import the Neo4j connector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

st.title("SocialGene Chat!")

# Set up the Neo4j connection using credentials (adjust as necessary)
neo4j_connector = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter your query:"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Execute the query using Neo4j
    results = neo4j_connector.execute_query(prompt)
    response = str(results)  # Convert results to string, adjust formatting as needed

    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    # Display assistant's message in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)

# Close the Neo4j connection when done
neo4j_connector.close()