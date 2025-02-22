import streamlit as st
import streamlit.components.v1 as components
import openai
import google.generativeai as genai
import replicate
import requests
import os
import time
import speech_recognition as sr
from deep_translator import GoogleTranslator

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
page = st.sidebar.radio("🔍 Navigation", ["Chat", "Voice Assistant", "How to Use"])

if page == "How to Use":
    st.title("📖 How to Use AI Chat UI")
    st.markdown("""
    Welcome to **AI Chat UI**! Here's how to use different features:

    1️⃣ **Basic Chat:** `"Tell me a joke!"` → Select **OpenAI GPT**  
    2️⃣ **Persistent AI:** `"Remember my name is Alex"` → Select **OpenAI Assistant**  
    3️⃣ **Function Calling:** `"What’s the weather in New York?"` → Select **OpenAI GPT + Tools**  
    4️⃣ **Image Generation:** `"A futuristic robot on Mars"` → Select **DALL·E 3**  
    5️⃣ **Batch Speech-to-Text:** Upload multiple audio files → Select **Whisper (Speech-to-Text)**  
    6️⃣ **Live Speech-to-Text:** Click "Start Recording" → Select **Whisper (Live Speech)**  
    7️⃣ **Multilingual Transcription:** Select a language after transcribing.  
    8️⃣ **AI Voice Assistant:** Use **ElevenLabs** on the "Voice Assistant" page.  

    **💡 Tips:**
    - Enter API keys in the sidebar before using models.
    - Select a model before typing a message.
    - For **image generation**, enter a detailed prompt.
    - For **Whisper**, upload an **MP3, WAV, or M4A** file.

    🚀 Have fun experimenting!
    """)
    st.stop()

# ---- ElevenLabs AI Voice Assistant Page ----
if page == "Voice Assistant":
    st.title("🎤 ElevenLabs AI Voice Assistant")
    
    convai_html = """
    <elevenlabs-convai agent-id="07SRhAkpaGG5svmcKAlh"></elevenlabs-convai>
    <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    """
    components.html(convai_html, height=300)
    st.stop()  # Stop execution if on this page

# ---- Chat UI ----
st.title("🤖 AI Chat UI")

# Move Model Selection Above Input Box
model_choice = st.selectbox(
    "Choose AI Model:",
    ["OpenAI GPT", "OpenAI Assistant", "OpenAI GPT + Tools", "DALL·E 3 (Image Gen)",
     "Whisper (Speech-to-Text)", "Whisper (Live Speech)", "Google Gemini", "Replicate Llama", "Stable Diffusion"]
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
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = "🤖 AI: Sorry, no response yet."

    # OpenAI GPT Chat
    if model_choice == "OpenAI GPT" and openai_key:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_input}]
            ).choices[0].message.content
        except Exception as e:
            response = f"⚠️ OpenAI Error: {str(e)}"

    # OpenAI Whisper (Speech-to-Text)
    elif model_choice == "Whisper (Speech-to-Text)":
        st.subheader("🎙 Upload Audio Files for Transcription")
        
        uploaded_files = st.file_uploader("Upload multiple audio files (MP3, WAV, M4A)", 
                                          type=["mp3", "wav", "m4a"], accept_multiple_files=True)
        
        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    file_path = f"temp_{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.read())

                    with open(file_path, "rb") as f:
                        response = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=f
                        ).text

                    st.success(f"✅ Transcription for {uploaded_file.name}: {response}")

                    # Language translation option
                    target_lang = st.selectbox(f"Translate {uploaded_file.name} Transcription to:", 
                                               ["None", "French", "Spanish", "German", "Chinese"])
                    if target_lang != "None":
                        translated_text = GoogleTranslator(source="auto", target=target_lang.lower()).translate(response)
                        st.markdown(f"🌍 **Translated ({target_lang})**: {translated_text}")

                    st.session_state.messages.append({"role": "user", "content": f"📂 Uploaded: {uploaded_file.name}"})
                    st.session_state.messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    st.error(f"⚠️ Whisper Error: {str(e)}")

    # Display AI Response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Save AI Response to History
    st.session_state.messages.append({"role": "assistant", "content": response})
