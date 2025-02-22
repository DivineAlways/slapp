import streamlit as st
import openai
import google.generativeai as genai
import replicate
import requests
import os
import time

# ---- PAGE CONFIG ----
st.set_page_config(page_title="🤖 AI Chat UI", page_icon="💬")

# ---- Sidebar for API Keys ----
st.sidebar.title("🔑 API Keys & Settings")
openai_key = st.sidebar.text_input("🔑 OpenAI API Key", type="password")
google_key = st.sidebar.text_input("🔑 Google AI Key", type="password")
replicate_key = st.sidebar.text_input("🔑 Replicate API Key", type="password")
weather_api_key = st.sidebar.text_input("🌦 Weather API Key (Optional)", type="password")

# Set API keys
if openai_key:
    client = openai.OpenAI(api_key=openai_key)

if google_key:
    genai.configure(api_key=google_key)

if replicate_key:
    os.environ["REPLICATE_API_TOKEN"] = replicate_key

# ---- Function for Tools ----
def get_weather(city):
    if not weather_api_key:
        return "⚠️ Please enter a Weather API Key in the sidebar."
    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
        response = requests.get(url).json()
        return f"🌦 Current temperature in {city}: {response['current']['temp_c']}°C"
    except:
        return "⚠️ Unable to fetch weather data."

# Define functions available to OpenAI
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"}
            },
            "required": ["city"]
        }
    }
]

# ---- Page Navigation ----
page = st.sidebar.radio("🔍 Navigation", ["Chat", "How to Use"])

if page == "How to Use":
    st.title("📖 How to Use AI Chat UI")
    st.markdown("""
    Welcome to **AI Chat UI**! Here's how to use different features:

    1️⃣ **Basic Chat:** `"Tell me a joke!"` → Select **OpenAI GPT**  
    2️⃣ **Persistent AI:** `"Remember my name is Alex"` → Select **OpenAI Assistant**  
    3️⃣ **Function Calling:** `"What’s the weather in New York?"` → Select **OpenAI GPT + Tools**  
    4️⃣ **Image Generation:** `"A futuristic robot on Mars"` → Select **DALL·E 3**  
    5️⃣ **Speech-to-Text:** Upload an audio file → Select **Whisper (Speech-to-Text)**  
    6️⃣ **Replicate LLaMA:** `"Explain Web3"` → Select **Replicate Llama**  
    7️⃣ **Replicate Stable Diffusion:** `"A neon cyberpunk warrior"` → Select **Stable Diffusion**  

    **💡 Tips:**
    - Enter API keys in the sidebar before using models.
    - Select a model before typing a message.
    - For **image generation**, enter a detailed prompt.
    - For **Whisper**, upload an **MP3 or WAV** file.

    🚀 Have fun experimenting!
    """)
    st.stop()

# ---- Chat UI ----
st.title("🤖 AI Chat UI")

# Move Model Selection Above Input Box
model_choice = st.selectbox(
    "Choose AI Model:",
    ["OpenAI GPT", "OpenAI Assistant", "OpenAI GPT + Tools", "DALL·E 3 (Image Gen)",
     "Whisper (Speech-to-Text)", "Google Gemini", "Replicate Llama", "Stable Diffusion"]
)

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

    response = "🤖 AI: Sorry, no response yet."

    # OpenAI GPT
    if model_choice == "OpenAI GPT" and openai_key:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            ).choices[0].message.content
        except Exception as e:
            response = f"⚠️ OpenAI Error: {str(e)}"

    # OpenAI Assistant (Persistent AI)
    elif model_choice == "OpenAI Assistant" and openai_key:
        try:
            if "assistant_id" not in st.session_state:
                assistant = client.beta.assistants.create(
                    name="LowPerry AI",
                    instructions="You're a helpful assistant for game dev and AI.",
                    tools=[],
                    model="gpt-4-turbo"
                )
                st.session_state.assistant_id = assistant.id

            if "thread_id" not in st.session_state:
                thread = client.beta.threads.create()
                st.session_state.thread_id = thread.id

            client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=user_input
            )

            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=st.session_state.assistant_id
            )

            # Wait for completion (Polling)
            while True:
                run_status = client.beta.threads.runs.retrieve(run.id)
                if run_status.status == "completed":
                    break
                time.sleep(2)

            messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
            response = messages.data[0].content[0].text.value

        except Exception as e:
            response = f"⚠️ OpenAI Assistant Error: {str(e)}"

    # OpenAI Function Calling (Weather API Example)
    elif model_choice == "OpenAI GPT + Tools":
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[{"role": "user", "content": user_input}],
                functions=functions
            ).choices[0].message.content
        except Exception as e:
            response = f"⚠️ OpenAI Tools Error: {str(e)}"

    # OpenAI Whisper (Speech-to-Text)
    elif model_choice == "Whisper (Speech-to-Text)":
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])
        if uploaded_file:
            try:
                file_path = f"temp_{uploaded_file.name}"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())

                with open(file_path, "rb") as f:
                    response = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=f
                    ).text
            except Exception as e:
                response = f"⚠️ Whisper Error: {str(e)}"

    # Display AI Response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save AI Response to History
    st.session_state.messages.append({"role": "assistant", "content": response})
