import streamlit as st
import requests

st.set_page_config(page_title="Enterprise AI Assistant", page_icon="🤖")
st.title("AI Assistant")

st.markdown("Ask me about HR or Finance 👇")

query = st.text_input("Your question:")

if query:
    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:5002/ask",
            json={"query": query}
        )
        if response.status_code == 200:
            st.success(response.json()["answer"])
        else:
            st.error("⚠️ Something went wrong.")