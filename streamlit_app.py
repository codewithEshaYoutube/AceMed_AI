import streamlit as st
from openai import OpenAI
import sqlite3

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
""")
conn.commit()

# App title and description
st.title("🩺 AceMed AI - MDCAT LMS Dashboard")
st.sidebar.image("Assets/Images/AceMed AI logo.jpg", caption="AceMed AI Logo", use_column_width=True)

st.sidebar.header("Dashboard Navigation")
page = st.sidebar.radio("Select a page", ["📚 Study Materials", "💬 MDCAT Chatbot", "📊 Performance Tracker"])

if page == "📚 Study Materials":
    st.subheader("📖 Study Materials")
    st.write("Access MDCAT subject-wise notes, past papers, and video lectures.")
    st.write("- **Biology**: Human Physiology, Genetics, Ecology")
    st.write("- **Chemistry**: Organic Chemistry, Periodic Table, Chemical Bonding")
    st.write("- **Physics**: Kinematics, Dynamics, Thermodynamics")
    st.write("- **English**: Grammar, Vocabulary, Comprehension")

elif page == "📊 Performance Tracker":
    st.subheader("📈 Performance Tracker")
    st.write("Track your MDCAT practice test scores and improvements over time.")
    st.line_chart([70, 75, 80, 85, 90, 95])

elif page == "💬 MDCAT Chatbot":
    st.subheader("💬 MDCAT AI Chatbot")
    st.write("AceMed AI is designed to assist MDCAT students with subject-related queries and explanations.")

    # Use dummy key for now
    openai_api_key = "1e7d1c3888be4ecc9d5e2b98981edc74"  # Dummy API Key
    
    # Create OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Initialize session state for storing messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input field
    if prompt := st.chat_input("Ask a question about MDCAT subjects..."):
        # Store and display user query
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Display AI response
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
