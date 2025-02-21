import streamlit as st
import openai
import google.generativeai as genai
import replicate
import os

# ---- PAGE CONFIG ----
st.set_page_config(page_title="🤖 AI Chat UI", page_icon="💬")

# ---- Sidebar for API Keys ----
st.sidebar.title("🔑 API Keys & Settings")
openai_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
google_key = st.sidebar.text_input("🔑 Google AI Key", type="password")
replicate_key = st.sidebar.text_input("🔑 Replicate API Key", type="password")

# Set API keys
if openai_key:
    client = openai.OpenAI(api_key=openai_key)

if google_key:
    genai.configure(api_key=google_key)

if replicate_key:
    os.environ["REPLICATE_API_TOKEN"] = replicate_key

# ---- Chat UI ----
st.markdown("<h1 style='text-align: center;'>🤖 AI Chat UI</h1>", unsafe_allow_html=True)

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
user_input = st.chat_input("Type your message...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Select AI Model
    model_choice = st.sidebar.selectbox("Choose AI Model:", ["OpenAI GPT", "Google Gemini", "Replicate Llama", "Stable Diffusion"])

    response = "🤖 AI: Sorry, no response yet."

    # OpenAI Chat Completion (Fixed for OpenAI v1.0+)
    if model_choice == "OpenAI GPT" and openai_key:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            ).choices[0].message.content
        except Exception as e:
            response = f"⚠️ OpenAI Error: {str(e)}"

    # Google Gemini (Bard)
    elif model_choice == "Google Gemini" and google_key:
        try:
            response = genai.ChatSession(model="gemini-pro").send_message(user_input)["text"]
        except Exception as e:
            response = f"⚠️ Google AI Error: {str(e)}"

    # Replicate Llama 2 Chat Model (Text-based AI)
    elif model_choice == "Replicate Llama" and replicate_key:
        try:
            st.sidebar.info("⏳ Calling Replicate LLaMA API...")
            output = replicate.run(
                "meta/llama-2-7b-chat",
                input={"prompt": user_input, "max_length": 200}
            )
            response = "".join(output)
        except Exception as e:
            response = f"⚠️ Replicate LLaMA Error: {str(e)}"

    # Replicate Stable Diffusion (Image Generation)
    elif model_choice == "Stable Diffusion" and replicate_key:
        try:
            st.sidebar.info("⏳ Generating image...")
            output = replicate.run(
                "stability-ai/stable-diffusion",
                input={"prompt": user_input}
            )
            response = output[0]  # Image URL
            st.image(response, caption="Generated Image")
        except Exception as e:
            response = f"⚠️ Replicate Image Error: {str(e)}"

    # Display AI Response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save AI Response to History
    st.session_state.messages.append({"role": "assistant", "content": response})
