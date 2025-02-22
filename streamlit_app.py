import streamlit as st
import requests

# Function to send a Discord notification
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/your-webhook-id"  # Replace with your actual webhook URL

def send_discord_notification(message: str):
    payload = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        st.success("Notification sent to Discord!")
    else:
        st.error(f"Failed to send notification. Status code: {response.status_code}")

# App header
st.title("Welcome to FastLearn: Mastering FastAPI & Webhooks")
st.write("In this course, you'll learn how to:")
st.write("- Build a simple **FastAPI** app.")
st.write("- Deploy it to **Vercel**.")
st.write("- Set up **Discord Webhooks** for notifications.")
st.write("- Create a **Streamlit app** to interact with the API.")

# Step 1: Building the FastAPI app
st.header("Step 1: Build Your FastAPI App")

st.write("""
    In this module, we will create a simple **FastAPI** app that exposes a `GET /` endpoint
    and a `POST /items/` endpoint to create items. You will also deploy it to **Vercel**.
""")

# Simulate creating the FastAPI app with a button
if st.button("Create FastAPI App"):
    st.code("""
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()

    class Item(BaseModel):
        name: str
        description: str = None

    @app.get("/")
    def read_root():
        return {"message": "Hello, FastLearn World!"}

    @app.post("/items/")
    def create_item(item: Item):
        return {"name": item.name, "description": item.description}
    """)
    st.write("Great! You've created your FastAPI app. Now deploy it on Vercel.")
    st.write("To deploy, follow the steps on [Vercel's documentation](https://vercel.com/docs) for Python apps.")

# Step 2: Deploying to Vercel
st.header("Step 2: Deploy to Vercel")

st.write("""
    After building the FastAPI app, you can deploy it to **Vercel**. Simply push your code to GitHub and link
    your repository to Vercel for automatic deployment.
    Once deployed, your app will be accessible online!
""")

# Simulate Vercel deployment process
if st.button("Deploy to Vercel"):
    st.write("You can deploy this app on Vercel. Here are the steps:")
    st.write("""
        1. Push your FastAPI app to GitHub.
        2. Go to [Vercel](https://vercel.com/) and link your GitHub repo.
        3. Vercel will automatically detect and deploy your FastAPI app.
        4. After deployment, you'll get a URL for your app.
    """)
    st.write("Your FastAPI app is now live on Vercel!")

# Step 3: Setting up Discord Webhook Notifications
st.header("Step 3: Set up Discord Webhook Notifications")

st.write("""
    In this step, you'll learn how to connect your FastAPI app with **Discord Webhooks**.
    You can trigger notifications every time an item is created in your FastAPI app.
""")

# Simulate sending a Discord notification when creating an item
item_name = st.text_input("Enter Item Name:")
item_description = st.text_area("Enter Item Description:")

if st.button("Create Item and Send Discord Notification"):
    if item_name:
        send_discord_notification(f"New item created: {item_name} - {item_description}")
        st.success(f"Item '{item_name}' created! Notification sent to Discord.")
    else:
        st.warning("Please enter an item name.")

# Final Step: Recap and Interactive Learning
st.header("Final Step: Recap & Interactive Learning")

st.write("""
    You've learned how to build a FastAPI app, deploy it on Vercel, and connect it to Discord webhooks.
    Here's what we've covered:
    - Creating a simple **FastAPI** app.
    - Deploying the app to **Vercel** for public access.
    - Sending notifications to **Discord** via webhooks when creating items.

### Next Steps:
- You can extend this app by adding more functionality like updating or deleting items.
- Explore more advanced topics like authentication and database integration.
""")

st.write("Thanks for learning with **FastLearn**! Keep building and experimenting.")
