import time
import feedparser
from twilio.rest import Client
import logging

# === SETTINGS ===
NEWS_API_KEY = 'f9adae143f4a4e738932ce3122d7ff31'  # Your News API Key
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886'  # Twilio Sandbox or Verified WhatsApp Number
ACCOUNT_SID = 'AC5499642e06a42b3977a8db6cb3c37ee9'  # Your Twilio SID
AUTH_TOKEN = '743c6b62e6e9065d8163abc43b7e9df1'  # Your Twilio Auth Token

# List of WhatsApp numbers to send the message to
WHATSAPP_NUMBERS = [
    'whatsapp:+919051770645',  # Add more numbers as needed
    'whatsapp:+919143271042',  # Another example
    'whatsapp:+918293312764'   # Yet another example
]

# Bengali News RSS Feed URL (Replace with any Bengali news RSS feed)
BENGALI_NEWS_RSS_URL = "https://rss.app/feeds/Q84ZSoIiO9dKiXlv.xml"  # Example for Bangla Tribune

# === SETUP LOGGING ===
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# === FETCH BENGALI NEWS ===
def get_bengali_news():
    try:
        logging.info("Fetching Bengali news...")
        feed = feedparser.parse(BENGALI_NEWS_RSS_URL)
        
        if len(feed.entries) == 0:
            logging.warning("No news entries found.")
            return None
        
        news_message = '🗞️ *বাঙ্গালি সংবাদ (Bengali News):*\n\n'
        
        for idx, entry in enumerate(feed.entries[:5], 1):  # Top 5 headlines
            title = entry.title
            link = entry.link
            news_message += f"{idx}. {title}\n"
            news_message += f"🔗 [পড়ুন]({link})\n\n"  # "Read" in Bengali
        
        return news_message
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return None

# === SEND WHATSAPP MESSAGE TO MULTIPLE NUMBERS ===
def send_whatsapp_message(message_body, phone_numbers):
    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        # Split message if it exceeds 1600 characters
        max_length = 1600
        message_parts = [message_body[i:i + max_length] for i in range(0, len(message_body), max_length)]
        
        # Send each part of the message to all phone numbers
        for number in phone_numbers:
            for part in message_parts:
                message = client.messages.create(
                    from_=TWILIO_WHATSAPP_NUMBER,
                    body=part,
                    to=number
                )
                logging.info(f"✅ News sent to {number}. Message SID: {message.sid}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")


# === MAIN SCRIPT ===
if __name__ == '__main__':
    while True:
        bengali_news = get_bengali_news()
        if bengali_news:
            send_whatsapp_message(bengali_news, WHATSAPP_NUMBERS)
        else:
            logging.warning("No news to send.")
        
        # Wait for 5 minutes (300 seconds) before sending the next notification
        logging.info("⏳ Waiting for the next update...")
        time.sleep(300)  # Wait for 5 minutes before running the next iteration
