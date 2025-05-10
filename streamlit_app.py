import streamlit as st
import sqlite3
import requests
import uuid
import json
from datetime import datetime

# API Configuration 
API_KEY = "xKQyEGwC.uCyxokv9TXGkDscfGZxVNrCLiJT7rIkv"
BASE_URL = "https://payload.vextapp.com/hook/ICYAJ67MIS/catch"

# Generate a unique channel token
def generate_channel_token():
    """Generate a unique channel token using timestamp and UUID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_id = uuid.uuid4().hex[:8]
    return f"acemedai_{timestamp}_{random_id}"

def query_llm(prompt, api_key=API_KEY, channel_token=None):
    """
    Send a query to the LLM API
    
    Args:
        prompt (str): The user's query
        api_key (str): API key for authentication
        channel_token (str, optional): Custom channel token, generates one if not provided
    
    Returns:
        str: API response or error message
    """
    # Use provided channel token or generate a new one
    token = channel_token or generate_channel_token()
    
    # Prepare URL with channel token
    url = f"{BASE_URL}/{token}"
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "Apikey": f"Api-Key {api_key}"
    }
    
    # Prepare data
    payload = {
        "payload": prompt,
        "env": "dev"
    }
    
    try:
        # Make API call
        response = requests.post(url, json=payload, headers=headers)
        
        # Check response
        if response.status_code == 200:
            st.session_state.last_token = token
            return response.text.strip()
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"⚠️ Exception occurred: {str(e)}"

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

# Initialize session state for token tracking
if "last_token" not in st.session_state:
    st.session_state.last_token = "acemedai_default"

# Page configuration with improved aesthetics
st.set_page_config(
    page_title="AceMed AI - MDCAT LMS Dashboard", 
    page_icon="Assets/Images/page-logo.png", 
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
            *{
            color:black;
            }
        /* Main styling */
        .main-header {
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 20px;
            font-family: 'Helvetica Neue', sans-serif;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #1E3A8A;
            color: white;
        }
        .css-1y1e1a8:hover {
            background-color: #2563EB;
        }
        
        /* Logo sizing */
        .sidebar-logo {
            display: block;
            margin: 0 auto;
            max-width: 120px !important;
            border-radius: 10px;
        }
        
        /* Chat UI improvements */
        .chat-card {
            background-color: #F5F7FF;
            border-radius: 15px;
            box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.05);
            padding: 20px;
            margin-bottom: 20px;
            
        }
        .chat-input {
            background-color: #E0EAFF;
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #1E3A8A;

        }
        .assistant {
            background-color: #EFF6FF;
            border-radius: 12px;
            padding: 12px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.05);
            border-left: 4px solid #3B82F6;
        }
        .user {
            background-color: #E0EAFF;
            border-radius: 12px;
            padding: 12px;
            border-left: 4px solid #1E3A8A;
        }
        
        /* Material cards */
        .material-card {
            background: linear-gradient(135deg, #1E3A8A, #3B82F6);
            color: white;
            border-radius: 15px;
            box-shadow: 0px 8px 12px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 15px;
            transition: transform 0.3s ease;
        }
        .material-card:hover {
            transform: translateY(-5px);
        }
        
        /* Buttons */
        .download-btn {
            background-color: #1E3A8A;
            border: none;
            padding: 10px 20px;
            color: white;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .download-btn:hover {
            background-color: #3B82F6;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Performance tracker */
        .performance-tracker {
            background: linear-gradient(to right, #EFF6FF, #DBEAFE);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            border-left: 4px solid #3B82F6;
        }
        
        /* Footer */
        .footer {
            background-color: #1E3A8A;
            color: white;
            text-align: center;
            padding: 15px;
            margin-top: 30px;
            font-size: 14px;
            border-radius: 10px;
        }
        .footer a {
            color: #BFDBFE;
            text-decoration: none;
            transition: color 0.3s ease;
        }
        .footer a:hover {
            color: #60A5FA;
            text-decoration: underline;
        }
        
        /* API info box */
        .api-info {
            background-color: #DBEAFE;
            border-radius: 10px;
            padding: 10px;
            margin-top: 10px;
            font-size: 12px;
            color: #1E40AF;
            border: 1px solid #3B82F6;
        }
        
        /* Stat cards */
        .stat-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 15px;
            border-top: 3px solid #3B82F6;
        }
        
        /* Subject pills */
        .subject-pill {
            display: inline-block;
            background: #BFDBFE;
            color: #1E40AF;
            padding: 5px 10px;
            border-radius: 15px;
            margin-right: 10px;
            margin-bottom: 10px;
            font-size: 14px;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <h1 style="
        color: white; 
        text-align: center;
        font-weight: bold; 
        font-size: 2.5rem;
        margin-top: 0;
    ">
        Crack the MDCAT — Score Higher with AI Precision.
    </h1>
""", unsafe_allow_html=True)
import streamlit as st

import base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Encode your local image
image_base64 = get_base64_image("Assets/Images/page-logo.png")

# Display logo + text in sidebar (same row)
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{image_base64}" width="40" style="margin-right: 10px;" />
        <span style="font-size: 20px; color: white; font-weight: bold;">AceMed AI</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.header("Dashboard ")
page = st.sidebar.radio("Select a page", [
    "💬 MDCAT Chatbot", 
    "📚 Study Materials", 
    "📊 Performance Tracker",

])

# Chatbot UI with Enhanced Aesthetics
if page == "💬 MDCAT Chatbot":
    st.markdown('<div class="chat-card"><h2>💬 MDCAT AI Chatbot</h2><p><strong>AceMed AI</strong> is designed to assist MDCAT students with subject-related queries and explanations.</p></div>', unsafe_allow_html=True)
    
    # Initialize session state for storing messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(f"<div class='{message['role']}'>{message['content']}</div>", unsafe_allow_html=True)

    # User input field with emoji and custom styles
    prompt = st.chat_input("Ask a question about MDCAT subjects...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(f"<div class='chat-input'>{prompt}</div>", unsafe_allow_html=True)

        # Show a loading spinner when the assistant is generating a response
        with st.spinner("Generating response... please wait."):
            # Generate AI response using our integrated API
            response = query_llm(prompt)
            
        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(f"<div class='assistant'>{response}</div>", unsafe_allow_html=True)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Show API info in a collapsible section
        with st.expander("API Request Information", expanded=False):
            st.markdown(f"<div class='api-info'>Last channel token: {st.session_state.last_token}</div>", unsafe_allow_html=True)

# Study Materials Page with improved UI
elif page == "📚 Study Materials":
    st.markdown('<div class="chat-card"><h2>📖 Study Materials</h2><p>Access MDCAT subject-wise notes, past papers, and video lectures.</p></div>', unsafe_allow_html=True)

    # Tabs for different subject areas
    tab1, tab2, tab3, tab4 = st.tabs(["Biology", "Chemistry", "Physics", "English"])
    
    with tab1:
        st.markdown("<h3>Biology Materials</h3>", unsafe_allow_html=True)
        
        # Subject pills
        st.markdown("""
            <div>
                <span class="subject-pill">Cell Biology</span>
                <span class="subject-pill">Human Physiology</span>
                <span class="subject-pill">Genetics</span>
                <span class="subject-pill">Ecology</span>
                <span class="subject-pill">Evolution</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="material-card">
                    <h4>Human Physiology</h4>
                    <p>Comprehensive notes on circulatory, digestive, and nervous systems</p>
                    <button class="download-btn">Download Notes</button>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="material-card">
                    <h4>Genetics & Evolution</h4>
                    <p>Study materials covering genetic inheritance, DNA structure, and evolutionary processes</p>
                    <button class="download-btn">Download Notes</button>
                </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h3>Chemistry Materials</h3>", unsafe_allow_html=True)
        
        # Subject pills
        st.markdown("""
            <div>
                <span class="subject-pill">Organic Chemistry</span>
                <span class="subject-pill">Inorganic Chemistry</span>
                <span class="subject-pill">Physical Chemistry</span>
                <span class="subject-pill">Biochemistry</span>
            </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
                <div class="material-card">
                    <h4>Organic Chemistry</h4>
                    <p>Notes on functional groups, reactions, and mechanisms</p>
                    <button class="download-btn">Download Notes</button>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="material-card">
                    <h4>Periodic Table & Bonding</h4>
                    <p>Complete guide to periodic trends and chemical bonding</p>
                    <button class="download-btn">Download Notes</button>
                </div>
            """, unsafe_allow_html=True)

    # Syllabus Download Button with improved styling
    st.markdown("<br><h3>Download MDCAT 2025 Syllabus</h3>", unsafe_allow_html=True)

    if st.button("📝 Get MDCAT 2025 Syllabus", key="syllabus_button"):
        st.markdown("""
            <a href="https://drive.google.com/file/d/1IrHxSV_cYN-RPpz8Jc8qEtUD9RXB-vhX/view?usp=sharing" target="_blank" class="download-btn" style="text-decoration:none;">
                Download Syllabus PDF
            </a>
        """, unsafe_allow_html=True)

# Performance Tracker Page with enhanced visualizations
elif page == "📊 Performance Tracker":
    st.markdown('<div class="chat-card"><h2>📈 Performance Tracker</h2><p>Track your MDCAT practice test scores and improvements over time.</p></div>', unsafe_allow_html=True)

    # Stats overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="stat-card">
                <h4>Average Score</h4>
                <h2 style="color:#1E40AF">83%</h2>
                <p>+5% from last month</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="stat-card">
                <h4>Tests Completed</h4>
                <h2 style="color:#1E40AF">12</h2>
                <p>3 this week</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="stat-card">
                <h4>Study Hours</h4>
                <h2 style="color:#1E40AF">48</h2>
                <p>10 hours this week</p>
            </div>
        """, unsafe_allow_html=True)

    # Performance chart
    st.markdown('<div class="performance-tracker"><h3>Your MDCAT Test Scores</h3></div>', unsafe_allow_html=True)
    
    import pandas as pd
    import numpy as np
    
    # Sample data for visualization
    dates = pd.date_range(start='2025-01-01', periods=6, freq='W')
    scores = [70, 75, 80, 85, 90, 95]
    
    # Creating a DataFrame
    df = pd.DataFrame({
        'Date': dates,
        'Score': scores,
        'Biology': [68, 72, 78, 82, 88, 92],
        'Chemistry': [65, 70, 75, 80, 85, 90],
        'Physics': [72, 78, 82, 86, 92, 96],
        'English': [75, 80, 85, 90, 95, 98]
    })
    
    # Overall score trend
    st.line_chart(df.set_index('Date')['Score'])
    
    # Subject-wise performance
    st.markdown('<h3>Subject-wise Performance</h3>', unsafe_allow_html=True)
    st.line_chart(df.set_index('Date')[['Biology', 'Chemistry', 'Physics', 'English']])
    
    # Radar chart for strengths and weaknesses
    st.markdown('<h3>Strength Areas</h3>', unsafe_allow_html=True)
    radar_data = {
        'Metrics': ['Cell Biology', 'Human Physiology', 'Organic Chemistry', 
                   'Inorganic Chemistry', 'Mechanics', 'Thermodynamics', 'Grammar', 'Vocabulary'],
        'Scores': [85, 92, 78, 82, 90, 75, 88, 94]
    }
    radar_df = pd.DataFrame(radar_data)
    
    st.bar_chart(radar_df.set_index('Metrics')['Scores'])

# API Settings Page
elif page == "⚙️ API Settings":
    st.markdown('<div class="chat-card"><h2>⚙️ API Configuration</h2><p>Configure the AI service and API settings.</p></div>', unsafe_allow_html=True)
    
    with st.form("api_settings"):
        custom_api_key = st.text_input("API Key", value=API_KEY, type="password")
        custom_channel = st.text_input("Custom Channel Token (optional)", 
                                      value=st.session_state.last_token if "last_token" in st.session_state else "")
        
        environment = st.selectbox("Environment", ["dev", "stage", "prod"], index=0)
        
        test_prompt = st.text_area("Test Prompt", value="What is the function of mitochondria in a cell?")
        
        submitted = st.form_submit_button("Test API Connection")
        
        if submitted:
            with st.spinner("Testing API connection..."):
                response = query_llm(test_prompt, api_key=custom_api_key, 
                                    channel_token=custom_channel if custom_channel else None)
                
            st.success("API connection successful!")
            st.markdown(f"<div class='assistant'>{response}</div>", unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class='api-info'>
                    <p><strong>Channel Token:</strong> {st.session_state.last_token}</p>
                    <p><strong>Status:</strong> Connected</p>
                </div>
            """, unsafe_allow_html=True)

st.markdown("""
    <div class="footer" >
        <p >&copy; 2025 AceMed AI - All rights reserved | <a href="https://www.linkedin.com/company/acemedai/">Follow Us on LinkedIn</a></p>
        <p>Made with ❤ by Eesha Tariq</p>
    </div>
""", unsafe_allow_html=True) 