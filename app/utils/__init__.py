from openai import OpenAI
import streamlit as st

UPSTAGE_API_KEY = st.secrets["UPSTAGE_API_KEY"]

client = OpenAI(api_key=UPSTAGE_API_KEY, base_url="https://api.upstage.ai/v1/solar")