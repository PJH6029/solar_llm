from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=st.secrets["UPSTAGE_API_KEY"], base_url="https://api.upstage.ai/v1/solar")