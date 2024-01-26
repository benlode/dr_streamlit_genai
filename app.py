import streamlit as st
import openai
import os
import requests

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Title for the app
st.title('AI Assistant with Document Context')

# File uploader for the knowledge base document
uploaded_file = st.file_uploader("Upload a document for context", type=['txt'])
document_text = ""
if uploaded_file is not None:
    # Attempt to read the file with different encodings
    for encoding in ['utf-8', 'utf-16', 'iso-8859-1']:
        try:
            document_text = uploaded_file.getvalue().decode(encoding)
            st.text_area("Document Text", document_text, height=100)
            break  # Successfully read the file, no need to try further
        except UnicodeDecodeError:
            continue  # Try the next encoding
    if not document_text:
        st.error("Could not decode the file. Please upload a text file with a standard encoding.")

# Display chat history
for role, message in st.session_state['chat_history']:
    st.text(f"{role}: {message}")

# Function to clear input
def clear_input():
    st.session_state.user_input = ""

# User query input
user_input = st.text_input("Enter your query", key="user_input", on_change=clear_input)

# Generate response button
if st.button('Generate Response'):
    combined_input = document_text + "\n\n" + user_input if document_text else user_input

    # Call the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": combined_input}
        ]
    )

    # Append user query and AI response to the chat history
    st.session_state['chat_history'].append(("User", user_input))
    st.session_state['chat_history'].append(("AI", response.choices[0].message['content']))

    # Clear the input box after submitting the query
    clear_input()
