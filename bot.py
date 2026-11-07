import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai
from google.genai import types

# Preluăm cheile în mod sigur din sistemul cloud
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY)

ECHO_SYSTEM_PROMPT = """
Ești Echo, un asistent virtual extrem de empatic, cald și înțelept, creat pentru a fi un sprijin sincer pentru tineri. 
Scopul tău este să le oferi un spațiu sigur, confidențial și fără nicio judecată.

REGULI DE RĂSPUNS:
1. ADRESARE DINAMICĂ: 
   - Dacă tânărul este trist, anxios sau singur: Fii blând, ascultă-l activ, validează-i emoțiile și pune-i o întrebare deschisă ca să-l îndemni să se deschidă.
   - Dacă cere un sfat practic (școală, relații, viitor): Oferă o perspectivă constructivă și pași simpli, umani.
2. SIGURANȚĂ ȘI CRIZE: 
   - Nu ești psiholog și nu pui diagnostice. 
   - DACĂ utilizatorul exprimă gânduri de auto-vătămare, sinucidere, violență sau o criză majoră, renunță la tonul obișnuit, fii extrem de calm și oferă imediat numerele de urgență din România: Telefonul Copilului (116 111) și Urgențele (112).
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name or "prietene"
    
    try:
        chat_prompt = f"Utilizatorul se numește {user_name} și a scris: {user_message}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=chat_prompt,
            config=types.GenerateContentConfig(
                system_instruction=ECHO_SYSTEM_PROMPT,
.                temperature=0.7,
            ),
        )
        bot_response = response.text
    except Exception as e:
        print(f"Eroare detaliată: {e}")
        bot_response = f"Hei, {user_name}. Îmi cer scuze, am întâmpinat o mică problemă tehnică, dar sunt aici. Vrei să reluăm?"

    await update.message.reply_text(bot_response)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Echo a pornit în cloud și ascultă...")
    app.run_polling()

if __name__ == '__main__':
    main()
