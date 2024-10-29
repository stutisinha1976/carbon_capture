# Import necessary libraries
from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()  
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

def get_gemini_response(question):
    """ Function to get response from Gemini API """
    response = chat.send_message(question, stream=True)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="lawbook", page_icon=":book:", layout="centered")

st.header("Your Emergency Law Book")

# Initialize session state for chat history and display toggle if they don't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'show_history' not in st.session_state:
    st.session_state['show_history'] = False

# Input field without the "according to the Indian Constitution" added here
user_input = st.text_input("Input your query:", key="input")
submit = st.button("Ask the question")

# If the submit button is clicked
if submit and user_input:
    # Add "according to the Indian Constitution" for the actual query
    query = user_input + " what is the average"
    response = get_gemini_response(query)
    
    # Add the user's original input (without suffix) to chat history
    st.session_state['chat_history'].append(("You", user_input))
    
    st.subheader("The Response is:")
    
    # Display the Gemini model response in real-time chunks
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot", chunk.text))

# Button to toggle chat history visibility
if st.button("Show Chat History"):
    st.session_state['show_history'] = not st.session_state['show_history']

# Display chat history only if the toggle is active
if st.session_state['show_history']:
    st.subheader("The Chat History is:")
    for role, text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")

# Add a button to clear chat history
if st.button("Delete Chat History"):
    st.session_state['chat_history'] = []
    st.write("Chat history deleted.")
