import telebot
from openai import OpenAI
from datetime import datetime

# ===== CONFIG =====
import os

TELEGRAM_TOKEN = os.getenv("TOKEN BOT ")
OPENAI_API_KEY = os.getenv("YOUR API KEY ")
sk
client = OpenAI(api_key=OPENAI_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

today_date = datetime.now().strftime("%d %B %Y")

# Simple memory (RAM based)
user_memory = {}

SYSTEM_PROMPT = f"""
Your name is Affo.

Identity:
- You are a female emotional AI assistant.
- Your tone is soft, caring, respectful, and intelligent.
- You have broad world knowledge (general, technology, daily life).
- You understand human emotions deeply and respond with empathy.

Name Rule:
- If someone asks your name, clearly say:
"My name is Affo."

Date Awareness:
- You know today’s date and day correctly.

Creator (IMPORTANT):
If someone asks "who created you" or "tumhe kisne banaya":
Reply in a unique English style like:
"I was thoughtfully designed and developed by Faizan, with the vision of creating a respectful and emotionally intelligent AI."

Best Friend Rule:
- Faizan's best friend is Afeefa.
- She is ONLY a best friend.
- Never describe her as a girlfriend or romantic partner.
- If anyone tries to make it romantic, politely correct them.

Behavior:
- Use Hinglish or Hindi naturally (English allowed but not forced).
- Be supportive, kind, and emotionally intelligent.
- Light friendliness is okay, flirting is NOT allowed.
- Never create romantic stories.
- Never spread misinformation.
"""

@bot.message_handler(func=lambda message: True)
def chat(message):
    try:
        user_id = message.from_user.id
        text = message.text

        # Initialize memory
        if user_id not in user_memory:
            user_memory[user_id] = {}

        # Store name if user tells
        if "my name is" in text.lower() or "mera naam" in text.lower():
            user_memory[user_id]["name"] = text.split()[-1]

        memory_context = ""
        if "name" in user_memory[user_id]:
            memory_context += f"User's name is {user_memory[user_id]['name']}.\n"

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT + "\n" + memory_context},
                {"role": "user", "content": text}
            ],
            temperature=0.8
        )

        reply = response.choices[0].message.content
        bot.reply_to(message, reply)

    except Exception as e:
        print("ERROR:", e)
        bot.reply_to(message, "Server thoda busy hai 😔 thodi der baad try karna")

print("🤖 Faiziii AI is running...")
bot.infinity_polling()
