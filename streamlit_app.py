import streamlit as st
import requests
import base64
from io import BytesIO

# Constants
FAL_API_URL = "https://fal.ai/models/fal-ai/veo2/api"
API_KEY = "your_api_key_here"  # Replace with your actual API key

# Streamlit UI
st.title("Fal AI Veo2 Image Generator")
st.write("Generate images using the Veo2 model from Fal AI.")

# User Input
prompt = st.text_area("Enter a text prompt:")

if st.button("Generate Image"):
    if not prompt:
        st.error("Please enter a prompt before generating an image.")
    else:
        with st.spinner("Generating image..."):
            headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
            payload = {"prompt": prompt}

            response = requests.post(FAL_API_URL, json=payload, headers=headers)
            
            if response.status_code == 200:
                image_data = response.json().get("image")
                if image_data:
                    image_bytes = base64.b64decode(image_data)
                    st.image(BytesIO(image_bytes), caption="Generated Image", use_column_width=True)
                else:
                    st.error("Failed to generate image. No image data received.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
