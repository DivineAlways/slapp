import streamlit as st
import fal_client
import os

# Streamlit UI
st.title("Fal AI Veo2 Image Generator")
st.write("Generate images using the Veo2 model from Fal AI.")

# API Key Input
api_key = st.text_input("Enter your API Key:", type="password").strip()

# User Input
prompt = st.text_area("Enter a text prompt:")

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            st.write(log["message"])

if st.button("Generate Image"):
    if not prompt:
        st.error("Please enter a prompt before generating an image.")
    elif not api_key:
        st.error("Please enter your API key.")
    else:
        with st.spinner("Generating image..."):
            try:
                os.environ["FAL_KEY"] = api_key  # Set API key as environment variable
                result = fal_client.subscribe(
                    "fal-ai/veo2",
                    arguments={"prompt": prompt},
                    with_logs=True,
                    on_queue_update=on_queue_update,
                )
                st.write(result)
            except Exception as e:
                st.error(f"Error occurred: {e}")
