import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load API key
load_dotenv()
api_key = os.getenv("")

if not api_key:
    st.error("❌ GROQ API key not found. Check your .env file")
    st.stop()

# Initialize LLM
llm = ChatGroq(
    groq_api_key=api_key,
    model_name="llama-3.1-8b-instant"
)

# Options
length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

# Sample tags (replace with FewShot later if needed)
tags = [
    "Artificial Intelligence",
    "Machine Learning",
    "Career Growth",
    "Startups",
    "Productivity",
    "Software Development"
]

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="🔗")

# 🔥 Backend logic (integrated here)
def generate_post(llm, length, language, topic):
    prompt = f"""
    Write a {length} LinkedIn post in {language} about {topic}.

    Make it:
    - Engaging with a strong hook
    - Professional tone
    - Include emojis if suitable
    - Add 3-5 relevant hashtags at the end
    """

    response = llm.invoke(prompt)
    return response.content


# UI
def main():
    st.subheader("🔗 LinkedIn Post Generator")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_tag = st.selectbox("Topic", options=tags)

    with col2:
        selected_length = st.selectbox("Length", options=length_options)

    with col3:
        selected_language = st.selectbox("Language", options=language_options)

    if st.button("Generate 🚀"):
        with st.spinner("Generating post..."):
            post = generate_post(llm, selected_length, selected_language, selected_tag)
            st.success("✅ Post Generated")
            st.write(post)


if __name__ == "__main__":
    main()