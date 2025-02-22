import streamlit as st

# Page Title
st.title("Unorthodox Streamlit Experiences")
st.markdown("Explore creative, interactive, and fun ways to use FastAPI with Streamlit!")

# Sidebar Navigation
st.sidebar.title("Select Experience")
option = st.sidebar.radio(
    "Choose an Experience",
    [
        "Scavenger Hunt",
        "AI Role-Playing Game",
        "Stock Market Simulation",
        "AI Interview Bot",
        "Collaborative Storytelling",
        "Music Jam Session",
        "Cybersecurity Challenges",
        "Digital Time Capsule",
        "Alternate Reality Game (ARG)",
        "Debate Simulation",
    ]
)

# Scavenger Hunt Section
if option == "Scavenger Hunt":
    st.header("Scavenger Hunt")
    st.markdown("In this scavenger hunt, you will solve **real-world clues** that are dynamically generated based on your progress!")
    st.markdown("### How it works:")
    st.markdown("1. Enter your answer to the clues.")
    st.markdown("2. Submit your answers to move to the next clue.")
    st.text_input("Enter your answer:")
    st.button("Submit Answer")

# AI Role-Playing Game Section
elif option == "AI Role-Playing Game":
    st.header("AI Role-Playing Game")
    st.markdown("Engage in an **AI-driven RPG** where the story evolves based on your choices.")
    st.markdown("### How it works:")
    st.markdown("1. Start your journey by typing your actions or choices.")
    st.markdown("2. The AI will generate new quests and challenges for you.")
    st.text_area("Start your journey:")
    st.button("Next Quest")

# Stock Market Simulation Section
elif option == "Stock Market Simulation":
    st.header("Stock Market Simulation")
    st.markdown("Trade in a **simulated stock market** and make decisions based on real stock data.")
    st.markdown("### How it works:")
    st.markdown("1. Select a stock from the list.")
    st.markdown("2. Enter the amount you'd like to trade.")
    st.markdown("3. Buy or sell stocks to simulate market activity.")
    st.selectbox("Select Stock", ["AAPL", "GOOG", "AMZN", "TSLA"])
    st.number_input("Enter Amount", min_value=1, max_value=100)
    st.button("Buy Stock")
    st.button("Sell Stock")

# AI Interview Bot Section
elif option == "AI Interview Bot":
    st.header("AI Interview Bot")
    st.markdown("Prepare for job interviews with an **AI-powered interview bot**.")
    st.markdown("### How it works:")
    st.markdown("1. The bot will ask you interview questions.")
    st.markdown("2. You respond, and the bot will analyze your answers in real-time.")
    st.text_area("Type your answer to the question:")
    st.button("Submit Answer")

# Collaborative Storytelling Section
elif option == "Collaborative Storytelling":
    st.header("Collaborative Storytelling")
    st.markdown("Join others to create a **collaborative story** where each player adds their part.")
    st.markdown("### How it works:")
    st.markdown("1. Type your contribution to the story.")
    st.markdown("2. The AI will generate the next part of the story for you.")
    st.text_area("Your story contribution:")
    st.button("Add to Story")

# Music Jam Session Section
elif option == "Music Jam Session":
    st.header("Music Jam Session")
    st.markdown("Create music with AI in a **jam session** that mixes your uploaded clips.")
    st.markdown("### How it works:")
    st.markdown("1. Upload a sound clip.")
    st.markdown("2. The AI will remix it and create a unique jam session for you.")
    st.file_uploader("Upload sound clip", type=["wav", "mp3"])
    st.button("Generate Remix")

# Cybersecurity Challenges Section
elif option == "Cybersecurity Challenges":
    st.header("Cybersecurity Challenges")
    st.markdown("Test your **cybersecurity skills** with challenges like cracking hashes or solving CTFs.")
    st.markdown("### How it works:")
    st.markdown("1. You will be given a cybersecurity puzzle.")
    st.markdown("2. Input your solution to crack the code or pass the challenge.")
    st.text_input("Enter the cracked password:")
    st.button("Submit")

# Digital Time Capsule Section
elif option == "Digital Time Capsule":
    st.header("Digital Time Capsule")
    st.markdown("Submit a **digital time capsule** and set a future date for it to be unlocked.")
    st.markdown("### How it works:")
    st.markdown("1. Type your message for the future.")
    st.markdown("2. Set a reveal date, and the capsule will be unlocked later.")
    st.text_area("Your message:")
    st.date_input("Set the reveal date:")
    st.button("Submit Capsule")

# Alternate Reality Game (ARG) Section
elif option == "Alternate Reality Game (ARG)":
    st.header("Alternate Reality Game (ARG)")
    st.markdown("Solve puzzles in the **real world** to progress in an ARG.")
    st.markdown("### How it works:")
    st.markdown("1. Input your solutions to physical-world puzzles.")
    st.markdown("2. Your progress will be tracked through the app.")
    st.text_input("Enter the puzzle solution:")
    st.button("Submit Solution")

# Debate Simulation Section
elif option == "Debate Simulation":
    st.header("Debate Simulation")
    st.markdown("Test your **debating skills** with AI opponents in real-time.")
    st.markdown("### How it works:")
    st.markdown("1. Enter your argument to debate a selected topic.")
    st.markdown("2. The AI will respond, and you can continue the debate.")
    st.text_area("Enter your argument:")
    st.button("Submit Argument")

# Footer
st.markdown("---")
st.markdown("Powered by Streamlit and FastAPI. Stay creative!")
