import streamlit as st
import openai
import requests
import random
import os

# Streamlit Page Config
st.set_page_config(page_title="Money Magic App", layout="wide")
st.title("🔮 Money Magic: A Chaos Magic Approach to Wealth")

# Sidebar Navigation
st.sidebar.title("📌 Navigation")
st.sidebar.markdown(
    '''
    <elevenlabs-convai agent-id="07SRhAkpaGG5svmcKAlh"></elevenlabs-convai>
    <script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
    ''',
    unsafe_allow_html=True
)
section = st.sidebar.radio("Go to", ["Chaos Magic Dashboard", "Sigil Generator", "Affirmation Generator", "Manifestation Journal", "Financial Data", "Subconscious Reprogramming"])

# User API Keys Input
st.sidebar.header("🔑 Enter Your API Keys")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
tiingo_api_key = st.sidebar.text_input("Tiingo API Key", type="password")
elevenlabs_api_key = st.sidebar.text_input("ElevenLabs API Key", type="password")

if not openai_api_key or not tiingo_api_key or not elevenlabs_api_key:
    st.sidebar.error("⚠️ Please enter all API keys before using the app.")

# OpenAI Affirmation Generator
def generate_affirmation(api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a manifestation coach. Generate a powerful financial affirmation."}]
    )
    return response["choices"][0]["message"]["content"]

# ElevenLabs Audio Generation
def generate_audio(api_key, text):
    url = "https://api.elevenlabs.io/v1/text-to-speech"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.7},
        "voice_id": "Rachel"
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        with open("affirmation.mp3", "wb") as f:
            f.write(response.content)
        return "affirmation.mp3"
    else:
        return None

# Chaos Magic Dashboard
if section == "Chaos Magic Dashboard":
    st.header("🔮 Welcome to Chaos Magic & Wealth Manifestation")
    st.write("Learn how to use Chaos Magic to enhance your financial success.")

# Sigil Generator
elif section == "Sigil Generator":
    st.header("✨ Sigil Generator")
    user_intent = st.text_input("Enter your financial intention (e.g., 'I attract wealth effortlessly'):")
    if st.button("Generate Sigil"):
        sigil = ''.join(random.sample(user_intent.replace(' ', ''), len(user_intent.replace(' ', ''))))
        st.success(f"Your sigil: {sigil.upper()}")

# Affirmation Generator
elif section == "Affirmation Generator":
    st.header("💬 AI-Powered Financial Affirmations")
    if openai_api_key and st.button("Generate Affirmation"):
        affirmation = generate_affirmation(openai_api_key)
        st.success(affirmation)

# Manifestation Journal
elif section == "Manifestation Journal":
    st.header("📖 Manifestation Journal")
    entry = st.text_area("Log your money magic ritual or manifestation experience:")
    if st.button("Save Entry"):
        with open("manifestation_journal.txt", "a") as file:
            file.write(entry + "\n---\n")
        st.success("Entry saved! Keep manifesting.")

# Financial Data (Using Tiingo API)
elif section == "Financial Data":
    st.header("📊 Real-Time Financial Data")
    ticker = st.text_input("Enter Stock/Crypto Symbol (e.g., AAPL, BTCUSD):", "AAPL")
    if tiingo_api_key and st.button("Get Data"):
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?token={tiingo_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.write(f"**{ticker} Price:** ${data[0]['close']}")
        else:
            st.error("Error fetching data. Check symbol and API key.")

# Subconscious Reprogramming (Audio from ElevenLabs)
elif section == "Subconscious Reprogramming":
    st.header("🎧 Wealth Mindset Reprogramming")
    affirmation_text = "Money flows to me effortlessly and abundantly. I am financially free."
    if elevenlabs_api_key and st.button("Generate & Play Audio"):
        audio_file = generate_audio(elevenlabs_api_key, affirmation_text)
        if audio_file:
            st.audio(audio_file)
        else:
            st.error("Failed to generate audio.")

st.write("🔮 Embrace Chaos Magic & Financial Success!")
