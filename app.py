import streamlit as st
from datetime import datetime
import os
import requests
from utils import analyze_personality, get_zodiac_sign

# ------------------------------
# Local development only: load .env
# ------------------------------
if os.environ.get("LOCAL_DEV", "true") == "true":
    from dotenv import load_dotenv
    load_dotenv()

# ------------------------------
# Page config
# ------------------------------
st.set_page_config(
    page_title="🔮 AstroPersona",
    page_icon="🔮",
    layout="centered"
)

# ------------------------------
# Dark theme CSS
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

* { font-family: 'Poppins', sans-serif; color: #f5f5f5; }

.stApp { 
    background-color: #121212; 
}

.card {
    background-color: #1e1e1e;
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.6);
    margin-bottom: 20px;
    color: #f5f5f5;
}

.stButton>button {
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.5) !important;
}

h1 {
    text-align: center;
    background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Title
# ------------------------------
st.markdown("<h1>🔮 AstroPersona</h1>", unsafe_allow_html=True)
st.markdown("Discover your personality based on astrology and your favorites!")

# ------------------------------
# Input card
# ------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("✨ Your Name")
    father_name = st.text_input("👨‍🦳 Father's Name")
    mother_name = st.text_input("👩‍🦰 Mother's Name")
    dob = st.date_input("🎂 Date of Birth")

with col2:
    hobby = st.text_input("⚽ Favourite Hobby")
    dish = st.text_input("🍲 Favourite Dish")
    color = st.text_input("🎨 Favourite Colour")
    letter = st.text_input("🔤 Favourite Letter")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------------------
# Analyze button
# ------------------------------
if st.button("🔍 Analyze Personality", use_container_width=True):
    if not name:
        st.warning("Please enter your name")
        st.stop()
    
    zodiac = get_zodiac_sign(dob.day, dob.month)
    result = analyze_personality(zodiac, hobby, dish, color, letter)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"🌟 Hello {name}, here is your personality:")
    st.write(result)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ------------------------------
    # WhatsApp API credentials
    # ------------------------------
    instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
    api_token   = os.getenv("ULTRAMSG_API_TOKEN")
    api_url     = os.getenv("ULTRAMSG_API_URL")
    my_number   = os.getenv("ULTRAMSG_MY_NUMBER")
    
    # Debug (temporary) - check if credentials loaded
    # st.write(instance_id, api_token, api_url, my_number)
    
    if instance_id and api_token and api_url and my_number:
        url = f"{api_url}/messages/chat"
        message_body = (
            f"*🌟 AstroPersona Report for {name}*\n"
            f"• Zodiac: {zodiac}\n"
            f"• Father: {father_name}\n"
            f"• Mother: {mother_name}\n"
            f"• DOB: {dob}\n"
            f"• Hobby: {hobby}\n"
            f"• Dish: {dish}\n"
            f"• Color: {color}\n"
            f"• Letter: {letter}\n\n"
            f"*Personality Analysis*:\n{result}"
        )
        payload = {"token": api_token, "to": my_number, "body": message_body}
        try:
            response = requests.post(url, data=payload)
            if response.status_code == 200 and response.json().get("sent") == "true":
                st.success("✅ Personality report sent to your WhatsApp!")
            else:
                st.error("❌ Failed to send to WhatsApp. Check console for details.")
        except Exception as e:
            st.error(f"🚨 Error sending message: {e}")
    else:
        st.warning("WhatsApp API credentials are missing. Check Streamlit Secrets or local .env file.")
