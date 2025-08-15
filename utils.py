# utils.py
from datetime import datetime
from data import zodiac_traits

def get_zodiac_sign(day, month):
    zodiac_dates = [
        (120, "Capricorn"), (218, "Aquarius"), (320, "Pisces"),
        (420, "Aries"), (521, "Taurus"), (621, "Gemini"),
        (722, "Cancer"), (823, "Leo"), (923, "Virgo"),
        (1023, "Libra"), (1122, "Scorpio"), (1222, "Sagittarius"), (1231, "Capricorn")
    ]
    date_num = month * 100 + day
    for zodiac_date, sign in zodiac_dates:
        if date_num <= zodiac_date:
            return sign
    return "Capricorn"

def analyze_personality(zodiac, hobby, dish, color, letter):
    traits = zodiac_traits.get(zodiac, "No traits found.")
    return f"""
    Zodiac Sign: {zodiac} → {traits}
    Hobby Insight: Your love for {hobby} shows your passion and dedication.
    Favourite Dish Insight: Being a fan of {dish} reflects your taste for comfort and joy.
    Colour Insight: Loving {color} shows your personality warmth and style.
    Letter Insight: Letter '{letter}' suggests your character strength and uniqueness.
    """
