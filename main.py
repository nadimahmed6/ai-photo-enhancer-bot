import os
import logging
import requests
import base64
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
HF_TOKEN = os.environ.get("HF_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to AI Photo Enhancer Bot!\n\n"
        "📸 Send me any photo and I'll enhance it to high quality using AI.\n\n"
        "✨ Powered by Real-ESRGAN AI Technology"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔍 How to use:\n\n"
        "1. Simply send any photo\n"
        "2. Wait a few seconds\n"
        "3. Receive your enhanced high-quality image!\n\n"
        "⚡ Best results with:\n"
        "• Old or blurry photos\n"
        "• Low resolution images\n"
        "• Dark or unclear pictures"
    )

async def enhance_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Enhancing your photo... Please wait!")
    
    try:
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        file_bytes = await file.download_as_bytearray()
        image_base64 = base64.b64encode(file_bytes).decode("utf-8")
        
        API_URL = "https://api-inference.huggingface.co/models/ai-forever/Real-ESRGAN"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {"inputs": image_base64}
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            await update.message.reply_photo(
                photo=response.content,
                caption="✅ Enhanced successfully!\n\n🤖 @aiphotoenhancer_bot"
            )
        else:
            await update.message.reply_text(
                "❌ Enhancement failed. Please try again with a different photo."
            )
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(
            "⚠️ Something went wrong. Please try again later."
        )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.PHOTO, enhance_photo))
    app.run_polling()

if __name__ == "__main__":
    main()
