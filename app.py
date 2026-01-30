import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# 1. SETUP PAGE
st.set_page_config(page_title="Iron Lady Career Catalyst", page_icon="💃", layout="centered")
st.title("💃 Iron Lady Career Catalyst")
st.markdown("---")

# 2. SIDEBAR FOR CONFIGURATION
with st.sidebar:
    st.header("Settings")
    google_api_key = st.text_input("Enter Google AI API Key", type="password", help="Get your key at aistudio.google.com")
    st.info("💡 **Mission:** Enabling 1 Million Women to reach the TOP!")
    st.markdown("[Visit Website](https://iamironlady.com)")

# 3. GUARDRAIL: STOP IF NO API KEY
if not google_api_key:
    st.warning("⚠️ Please enter your Google API Key in the sidebar to begin.")
    st.stop()

# 4. INITIALIZE GEMINI MODEL (Using 1.5-flash for stability)
# We add a try-except here to catch 429 Rate Limit errors gracefully
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
except Exception as e:
    st.error(f"Initialization Error: {e}")
    st.stop()

# 5. ENRICHED BUSINESS CONTEXT (Based on Iron Lady Research)
context = """
You are the 'Iron Lady Career Catalyst', an expert AI advisor for Iron Lady.
Iron Lady is India's leading leadership platform for women with 5+ years of experience.
Our founders are Rajesh Bhat and Suvarna Hegde.

CORE PHILOSOPHY:
- 'Business War Tactics': Strategies to win at work without fighting.
- 'Unapologetic Winning': Rejecting the idea that women must 'balance' or 'compromise' their ambitions.
- 'Strength-Based Excellence': Focusing on what you are great at to become indispensable.

PROGRAMS:
1. Leadership Essentials Program (4 Weeks): Masters 27 Business War Tactics. Focuses on confidence, pitching, and office politics.
2. 100 Board Members (6 Months): For mid-level women to fast-track to CXO and Board roles.
3. Master of Business Warfare (1 Year): The '1 Crore+ Club' for senior leaders aiming for the absolute top.

TONE: Bold, supportive, authoritative, and unapologetic.
"""

# 6. CHAT HISTORY MANAGEMENT
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. CHAT INTERACTION
if prompt := st.chat_input("Ex: How can I handle office politics?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Combine identity, context, and the user prompt
        full_instruction = f"{context}\n\nUser Question: {prompt}\n\nResponse:"
        
        try:
            # Generate response from Gemini
            response = llm.invoke(full_instruction)
            st.markdown(response.content)
            # Add assistant message to state
            st.session_state.messages.append({"role": "assistant", "content": response.content})
        except Exception as e:
            if "429" in str(e):
                st.error("🚦 **Rate Limit Reached:** The AI is taking a breath. Please wait 60 seconds before asking another question.")
            else:
                st.error(f"An error occurred: {e}")