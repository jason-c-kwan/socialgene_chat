import streamlit as st
from models.neo4j_model import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

def load_css(file_path):
    with open(file_path, "r") as file:
        return file.read()

def render_message(sender, message, is_user=True):
    sender_label = "User" if is_user else "Assistant"
    message_class = "user-message" if is_user else "assistant-message"
    return f"""
        <div class="{message_class}">
            <div class="message-bubble">
                <strong>{sender_label}:</strong> {message}
            </div>
        </div>
    """

def main():
    st.set_page_config(page_title="Neo4j Chat Interface", layout="wide")
    st.title("Neo4j Chat Interface")

    # Load and inject CSS
    css_content = load_css("static/css/styles.css")
    st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

    # Connect to Neo4j
    neo4j_connector = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    chat_history = []
    # Reset condition for the input field
    input_value = "" if st.session_state.get('reset_input', False) else st.session_state.get('user_input', "")
    user_input = st.text_input("Enter your message:", value=input_value, key="user_input", on_change=lambda: st.session_state.update({'send_message': True}))

    if st.session_state.get('send_message', False):
        chat_history.append(render_message("You", user_input, is_user=True))
        chat_container = st.empty()
        chat_container.markdown("".join(chat_history), unsafe_allow_html=True)

        query = user_input
        results = neo4j_connector.execute_query(query)
        response = str(results)

        chat_history.append(render_message("Assistant", response, is_user=False))
        chat_container.markdown("".join(chat_history), unsafe_allow_html=True)

        # Reset the input box by updating the session state
        st.session_state['user_input'] = ""
        st.session_state['reset_input'] = True
        st.session_state.send_message = False

    neo4j_connector.close()

if __name__ == "__main__":
    main()