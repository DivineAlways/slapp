import streamlit as st
import requests
import base64
from io import BytesIO

# Streamlit UI
st.title("Fal AI Veo2 Image Generator")
st.write("Generate images using the Veo2 model from Fal AI.")

# API Key Input
api_key = st.text_input("Enter your API Key:", type="password")

# User Input
prompt = st.text_area("Enter a text prompt:")

if st.button("Generate Image"):
    if not prompt:
        st.error("Please enter a prompt before generating an image.")
    elif not api_key:
        st.error("Please enter your API key.")
    else:
        with st.spinner("Generating image..."):
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"prompt": prompt}
            FAL_API_URL = "https://fal.ai/models/fal-ai/veo2/api"
            
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
