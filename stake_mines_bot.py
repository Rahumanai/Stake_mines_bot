import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# Set your bot token here
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Command: Start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm a Stake Mines Predictor bot.")

# Command: Predict
async def predict(update: Update, context: CallbackContext):
    await update.message.reply_text("Predicting safe tiles for Stake Mines...")

# Create the bot application
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
