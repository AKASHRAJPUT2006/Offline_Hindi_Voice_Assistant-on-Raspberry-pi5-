import datetime
import os
import json

# store last response globally
LAST_RESPONSE = "अभी कुछ कहा नहीं गया है।"

COMMANDS = {
    "GET_TIME": ["समय बताओ", "टाइम ", "टाइम बताओ","समय"],
    "GET_DATE": ["आज की तारीख क्या है", "तारीख बताओ", "दिनांक बताओ", "तारीख "],
    "GET_DAY": ["आज कौन सा दिन है", "आज का दिन बताओ"," दिन "," दिन बताओ"],
    "GREETING": ["नमस्ते", "हेलो", "हाय"],
    "INTRO": ["तुम कौन हो", "अपना परिचय दो","परिचय"],
    "THANKS": ["धन्यवाद", "थैंक यू"],
    "WEATHER": ["मौसम बताओ", "आज का मौसम क्या है","मौसम"],
    "HOW_ARE_YOU": ["कैसे हो", "क्या हाल है"],
    "HELP": [ " मेरी मदद करो"],
    "REPEAT": ["दोहराओ", "फिर से बोलो","फिर से"],
    "CAPABILITIES": ["तुम क्या कर सकते हो", "तुम क्या काम करते हो"],
    "UPTIME": ["कितनी देर से चालू हो", "अपटाइम बताओ","कितनी देर से चालू ", "कितनी देर से"],
    "EXIT": ["बंद हो जाओ", "रुको", "अलविदा"]
}

def normalize_text(text):
    text = text.strip()
    text = text.replace("हे", "है")
    text = text.replace("बताइए", "बताओ")
    return text

def recognize_intent(text):
    text = normalize_text(text)
    for intent, phrases in COMMANDS.items():
        for phrase in phrases:
            if phrase in text:
                return intent
    return "UNKNOWN"

# ---------- WEATHER (OFFLINE) ----------
def get_offline_weather():
    try:
        with open("weather_cache.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        return (
            f"{data['summary']}। "
            f"वर्तमान तापमान {data['temperature']} डिग्री सेल्सियस है। "
            f"अंतिम अपडेट: {data.get('last_updated', 'अज्ञात समय')}।"
        )

    
    except Exception:
        return "माफ़ कीजिए, ऑफलाइन मौसम जानकारी उपलब्ध नहीं है।"


# ---------- INTENT HANDLER ----------
def handle_intent(intent):
    global LAST_RESPONSE
    now = datetime.datetime.now()

    if intent == "GET_TIME":
        LAST_RESPONSE = f"अभी समय है {now.hour} बजकर {now.minute} मिनट"
        return LAST_RESPONSE

    if intent == "GET_DATE":
        LAST_RESPONSE = f"आज की तारीख है {now.day}-{now.month}-{now.year}"
        return LAST_RESPONSE

    if intent == "GET_DAY":
        LAST_RESPONSE = f"आज दिन है {now.strftime('%A')}"
        return LAST_RESPONSE

    if intent == "GREETING":
        LAST_RESPONSE = "नमस्ते, मैं आपका हिंदी सहायक हूँ।"
        return LAST_RESPONSE

    if intent == "INTRO":
        LAST_RESPONSE = "मैं रास्पबेरी पाई पर चलने वाला आपका ऑफलाइन हिंदी सहायक  हूँ"
        return LAST_RESPONSE

    if intent == "THANKS":
        LAST_RESPONSE = "आपका स्वागत है"
        return LAST_RESPONSE

    if intent == "WEATHER":
       LAST_RESPONSE = "एक क्षण कृपया। मैं ऑफलाइन मौसम जानकारी देख रहा हूँ। " + get_offline_weather()
       return LAST_RESPONSE


    if intent == "REPEAT":
        return LAST_RESPONSE
        
        
    if intent == "HOW_ARE_YOU":
        LAST_RESPONSE = "मैं ठीक हूँ, धन्यवाद। आप कैसे हैं?"
        return LAST_RESPONSE
    
        
        
    if intent == "CAPABILITIES":
        LAST_RESPONSE = (
            "मैं समय, तारीख, मौसम,  और सामान्य सवालों में मदद कर सकता हूँ।"
        )
        return LAST_RESPONSE
        
        
    if intent == "UPTIME":
        uptime = os.popen("uptime -p").read().strip()
        LAST_RESPONSE = f"मैं {uptime} से आपकी सेवा कर रहा हूँ।"
        return LAST_RESPONSE
        

    if intent == "HELP":
        LAST_RESPONSE = "मैं आपकी मदद करने के लिए तैयार हूँ। बताइए, आप मुझसे क्या चाहते हैं?ं"
        return LAST_RESPONSE

    if intent == "EXIT":
        LAST_RESPONSE = "ठीक है, फिर मिलेंगे। फिलहाल के लिए मैं बंद हो रहा हूँ।"
        return LAST_RESPONSE

    LAST_RESPONSE = "माफ कीजिए, मैं समझ नहीं पाया। कृपया दोबारा बोलिए।"
    return LAST_RESPONSE
