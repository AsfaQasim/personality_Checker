import streamlit as st
from datetime import datetime, date
import os
import requests
from utils import analyze_personality, get_zodiac_sign

# .env

if os.environ.get("LOCAL_DEV", "true") == "true":
    from dotenv import load_dotenv
    load_dotenv()


st.set_page_config(
    page_title="🔮 AstroPersona",
    page_icon="🔮",
    layout="centered"
)

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

/* Date input box */
.stDateInput input {
    color: black !important;
    font-weight: 600 !important;
    background: white !important;
    border-radius: 8px !important;
    padding: 6px !important;
}/* ✅ Force every text in datepicker to be pure black */
div[role="dialog"] .react-datepicker,
div[role="dialog"] .react-datepicker * {
    color: #000000 !important;   /* Pure black */
}

/* ✅ Specific date styles */
div[role="dialog"] .react-datepicker__day,
div[role="dialog"] .react-datepicker__day-name,
div[role="dialog"] .react-datepicker__current-month,
div[role="dialog"] .react-datepicker__day--outside-month {
    color: #000000 !important;   /* Force black */
    font-weight: 600 !important;
}


</style>
""", unsafe_allow_html=True)


st.markdown("<h1>🔮 AstroPersona</h1>", unsafe_allow_html=True)
st.markdown("Discover your personality based on astrology and your favorites!")


st.markdown('<div class="card">', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("✨ Your Name")
    father_name = st.text_input("👨‍🦳 Father's Name")
    mother_name = st.text_input("👩‍🦰 Mother's Name")
    dob = st.date_input(
        "🎂 Date of Birth",
        min_value=date(1980, 1, 1),
        max_value=date(2025, 12, 31)
    )

with col2:
    hobby = st.text_input("⚽ Favourite Hobby")
    dish = st.text_input("🍲 Favourite Dish")
    color = st.text_input("🎨 Favourite Colour")
    letter = st.text_input("🔤 Favourite Letter")

st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔍 Analyze Personality", use_container_width=True):
 
    if not all([name, father_name, mother_name, hobby, dish, color, letter, dob]):
        st.warning("⚠️ Please fill in all fields before proceeding!")
        st.stop()

    if dob.year < 1999 or dob.year > 2025:
        st.error("⚠️ Date of Birth must be between 1999 and 2025!")
        st.markdown(
            f"<p style='color:black; font-weight:bold;'>❌ Invalid Date: {dob}</p>",
            unsafe_allow_html=True
        )
        st.stop()

    
    zodiac = get_zodiac_sign(dob.day, dob.month)
    result = analyze_personality(zodiac, hobby, dish, color, letter)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader(f"🌟 Hello {name}, here is your personality:")
    st.write(result)
    st.markdown('</div>', unsafe_allow_html=True)

  
    instance_id = os.getenv("ULTRAMSG_INSTANCE_ID")
    api_token   = os.getenv("ULTRAMSG_API_TOKEN")
    api_url     = os.getenv("ULTRAMSG_API_URL")
    my_number   = os.getenv("ULTRAMSG_MY_NUMBER")

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
