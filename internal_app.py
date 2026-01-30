import streamlit as st
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
import os

st.set_page_config(page_title="Iron Lady Admin", layout="wide")
st.title("💼 Internal Lead Management System")

# Setup Model for AI Scoring
google_api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# Simple CSV Database
DB_FILE = "leads.csv"
if not os.path.exists(DB_FILE):
    pd.DataFrame(columns=["Name", "Email", "Exp", "AI_Score", "Status"]).to_csv(DB_FILE, index=False)

# --- CRUD Operations ---
tab1, tab2 = st.tabs(["➕ Add Lead", "📋 Manage Leads"])

with tab1:
    with st.form("add_lead"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        exp = st.number_input("Years of Exp", 0, 40)
        submitted = st.form_submit_button("Register Lead")
        
        if submitted and google_api_key:
            
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key)
            # logic: Scoring the lead
            score_prompt = f"Based on {exp} years of experience for a leadership program, give a 1-sentence 'Potential' rating."
            ai_rating = llm.invoke(score_prompt).content
            
            df = pd.read_csv(DB_FILE)
            new_row = pd.DataFrame([[name, email, exp, ai_rating, "New"]], columns=df.columns)
            pd.concat([df, new_row]).to_csv(DB_FILE, index=False)
            st.success("Lead Added with AI Insights!")

with tab2:
    df = pd.read_csv(DB_FILE)
    edited_df = st.data_editor(df, num_rows="dynamic")
    if st.button("Save Updates"):
        edited_df.to_csv(DB_FILE, index=False)
        st.success("Database Updated!")