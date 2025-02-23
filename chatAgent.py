import streamlit as st
import requests
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)

API_URL = "https://documentchatbot-production.up.railway.app/chat"  # Update with the correct API URL if needed

def main():
    st.title("Bartlesville HS Handbook Chatbot")
    
    user_query = st.text_input("Ask a question:")
    model_choice = st.selectbox("Choose a model:", ["mistral", "deepseek"])

    if st.button("Submit"):
        if user_query:
            response = send_query(user_query, model_choice)
            if response:
                st.success(response.get("response", "No response from the API."))
            else:
                st.error("Error in getting response from the API.")
        else:
            st.warning("Please enter a query.")

def send_query(query, model):
    payload = {
        "query": query,
        "model": model
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    main()
