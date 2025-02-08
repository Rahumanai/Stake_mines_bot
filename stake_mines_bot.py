from keep_alive import keep_alive
keep_alive()
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

# Get token from environment variables
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Configuration
CHANNEL_ID = "Aviatorsignalby"
ADMIN_USERNAME = "AnsonAA1"
BOT_PASSWORD = "ARMINES7448"
from datetime import datetime, timedelta
import json

verified_users = {}
channel_members = {}
user_stats = {}
daily_rewards = {}
vip_users = set()

def save_user_data():
    with open('user_data.json', 'w') as f:
        data = {
            'stats': user_stats,
            'daily': daily_rewards,
            'vip': list(vip_users)
        }
        json.dump(data, f)

def load_user_data():
    try:
        with open('user_data.json', 'r') as f:
            data = json.load(f)
            return data.get('stats', {}), data.get('daily', {}), set(data.get('vip', []))
    except:
        return {}, {}, set()

user_stats, daily_rewards, vip_users = load_user_data()

# Command: Start
async def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_ID}")],
        [InlineKeyboardButton("âœ… Verify Membership", callback_data='verify')],
        [InlineKeyboardButton("ðŸ‘¤ Profile", callback_data='profile'),
         InlineKeyboardButton("â“ Help", callback_data='help')],
        [InlineKeyboardButton("ðŸŽ¨ Themes", callback_data='themes'),
         InlineKeyboardButton("ðŸ‘‘ VIP Status", callback_data='vip')],
        [InlineKeyboardButton("ðŸ“Š Statistics", callback_data='stats'),
         InlineKeyboardButton("ðŸ”— Referral", callback_data='refer')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "ðŸŽ® Welcome to Stake Mines Predictor!\n\n"
        "Please follow these steps:\n"
        "1. Join our channel\n"
        "2. Click Verify Membership\n"
        "3. Enter the password: ARMINES7448\n\n"
        f"For help contact: {ADMIN_USERNAME}"
    )

    try:
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    except Exception as e:
        logger.error(f"Start command error: {str(e)}")
        await update.message.reply_text("An error occurred. Please try /start again.")

#Command: Help (Placeholder)
async def daily_reward(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in verified_users:
        await update.message.reply_text("Please verify yourself first!")
        return

    now = datetime.now()
    last_claim = datetime.fromisoformat(daily_rewards.get(str(user_id), '2000-01-01'))

    if now - last_claim < timedelta(days=1):
        next_claim = last_claim + timedelta(days=1)
        await update.message.reply_text(f"Next reward available in {next_claim - now}")
        return

    bonus = 2 if user_id in vip_users else 1
    daily_rewards[str(user_id)] = now.isoformat()
    user_stats[str(user_id)] = user_stats.get(str(user_id), 0) + (10 * bonus)
    save_user_data()

    await update.message.reply_text(f"Daily reward claimed: {10 * bonus} points!")

async def stats_command(update: Update, context: CallbackContext):
    user_id = str(update.message.from_user.id)
    points = user_stats.get(user_id, 0)
    vip_status = "VIP" if int(user_id) in vip_users else "Regular"

    await update.message.reply_text(
        f"ðŸ† Your Stats:\n"
        f"Points: {points}\n"
        f"Status: {vip_status}\n"
        f"Predictions Made: {user_stats.get(f'{user_id}_predictions', 0)}"
    )

async def help_command(update: Update, context: CallbackContext):
    help_text = (
        "ðŸŽ® Bot Commands:\n"
        "/start - Start the bot\n"
        "/daily - Claim daily reward\n"
        "/stats - View your statistics\n"
        "/help - Show this message\n\n"
        "VIP users get 2x daily rewards!"
    )
    await update.message.reply_text(help_text)

#Command: Profile (Placeholder)
async def profile_command(update:Update, context:CallbackContext):
    await update.message.reply_text("This is your profile. Contact @AnsonAA1 for assistance.")


async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if 'server_seed' not in context.user_data:
        context.user_data['server_seed'] = None

    if query.data == 'verify':
        try:
            chat_member = await context.bot.get_chat_member(f"@{CHANNEL_ID}", user_id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                channel_members[user_id] = True
                await query.message.reply_text(
                    "âœ… Channel verification successful!\n"
                    "Please enter the password to continue using the bot."
                )
            else:
                await query.message.reply_text(
                    "âŒ You need to join our channel first!\n"
                    f"Channel link: https://t.me/{CHANNEL_ID}"
                )
        except Exception as e:
            logger.error(f"Verification error: {str(e)}")
            await query.message.reply_text(
                "âŒ Verification failed. Please try again.\n"
                f"Channel link: https://t.me/{CHANNEL_ID}"
            )
    elif query.data == 'profile':
        await query.message.reply_text(
            "ðŸŽ® Your Profile:\n"
            f"User ID: {user_id}\n"
            f"Verified: {'Yes' if user_id in verified_users else 'No'}\n"
            f"For support contact: @{ADMIN_USERNAME}"
        )
    elif query.data == 'help':
        await query.message.reply_text(
            "ðŸŽ® Bot Help:\n"
            "1. Join our channel\n"
            "2. Verify your membership\n"
            "3. Enter the password\n"
            "4. Select mines count\n"
            "5. Enter server seed\n\n"
            f"For support contact: @{ADMIN_USERNAME}"
        )

    if query.data == 'verify':
        try:
            chat_member = await context.bot.get_chat_member(f"@{CHANNEL_ID}", user_id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                channel_members[user_id] = True
                await query.answer("âœ… Channel verification successful!")
                await query.message.reply_text(
                    "âœ… Channel verification successful!\n"
                    "Please enter the password to continue using the bot."
                )
            else:
                await query.answer("âŒ Please join our channel first!")
                await query.message.reply_text(
                    "âŒ You need to join our channel first!\n"
                    f"Channel link: https://t.me/{CHANNEL_ID}"
                )
        except Exception as e:
            logger.error(f"Verification error: {str(e)}")
            await query.message.reply_text(
                "âŒ Please make sure you've joined our channel!\n"
                f"Channel link: https://t.me/{CHANNEL_ID}"
            )
    elif query.data == 'profile':
        await query.message.reply_text("This is your profile. Contact @AnsonAA1 for assistance.")
    elif query.data == 'help':
        await query.message.reply_text("This is a help message. Contact @AnsonAA1 for assistance.")
    elif query.data == 'themes':
        keyboard = [[InlineKeyboardButton(theme.title(), callback_data=f'theme_{theme}')] for theme in themes.keys()]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select your prediction theme:", reply_markup=reply_markup)
    elif query.data.startswith('theme_'):
        theme = query.data.split('_')[1]
        user_themes[str(query.from_user.id)] = theme
        await query.message.reply_text(f"Theme changed to {theme.title()}!")
    elif query.data == 'refer':
        referral_code = f"MINES{query.from_user.id}"
        referral_link = f"https://t.me/your_bot_username?start={referral_code}"
        await query.message.reply_text(f"Share your referral link:\n{referral_link}")
    elif query.data == 'turbo_mode':
        if user_id not in vip_users:
            await query.answer("VIP feature only!")
            return
        context.user_data['turbo_mode'] = not context.user_data.get('turbo_mode', False)
        await query.answer(f"Turbo mode {'enabled' if context.user_data.get('turbo_mode') else 'disabled'}")
        return

    elif query.data.startswith('mines_'):
        if user_id not in verified_users:
            await query.answer("Please verify yourself first!")
            return

        if query.data == 'coming_soon':
            await query.answer("More mine options will be available soon!")
            return

        num_mines = int(query.data.split('_')[1])
        if context.user_data.get('server_seed') is None:
            await query.message.reply_text("Please enter your active server seed to continue:")
            context.user_data['pending_mines'] = num_mines
            return

        import random
        # Add random suffix to seed to get different positions each time
        current_seed = context.user_data['server_seed'] + str(random.randint(1, 999999))
        grid = generate_mines_prediction(num_mines, current_seed)
        prediction_text = format_prediction(grid)
        keyboard = [
            [InlineKeyboardButton("ðŸŽ² Next Prediction", callback_data=f'mines_{num_mines}')],
            [InlineKeyboardButton("â¬…ï¸ Back to Mine Selection", callback_data='back_to_mines')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            f"ðŸŽ® Stake Mines Prediction\n"
            f"Number of mines: {num_mines}\n\n"
            f"{prediction_text}\n\n"
            f"âš ï¸ Red: Bad mines (ðŸ’£)\n"
            f"âœ… Green: Safe diamonds (ðŸ’Ž)\n\n"
            f"Contact {ADMIN_USERNAME} for help",
            reply_markup=reply_markup
        )
    elif query.data == 'back_to_mines':
        keyboard = [
            [InlineKeyboardButton(f"{i} Mines", callback_data=f'mines_{i}') for i in range(1, 4)],
            [InlineKeyboardButton(f"{i} Mines", callback_data=f'mines_{i}') for i in range(4, 7)],
            [InlineKeyboardButton(f"{i} Mines", callback_data=f'mines_{i}') for i in range(7, 10)],
            [InlineKeyboardButton("10 Mines", callback_data='mines_10')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Select number of mines:", reply_markup=reply_markup)
        await query.message.delete()


async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in verified_users and 'pending_mines' in context.user_data:
        context.user_data['server_seed'] = update.message.text
        num_mines = context.user_data['pending_mines']
        del context.user_data['pending_mines']
        import random
        # Add random suffix to seed to get different positions each time
        current_seed = context.user_data['server_seed'] + str(random.randint(1, 999999))
        grid = generate_mines_prediction(num_mines, current_seed)
        prediction_text = format_prediction(grid)
        keyboard = [
            [InlineKeyboardButton("ðŸŽ² Next Prediction", callback_data=f'mines_{num_mines}')],
            [InlineKeyboardButton("â¬…ï¸ Back to Mine Selection", callback_data='back_to_mines')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"ðŸŽ® Stake Mines Prediction\n"
            f"Number of mines: {num_mines}\n"
            f"Server Seed: {context.user_data['server_seed']}\n\n"
            f"{prediction_text}\n\n"
            f"âš ï¸ Red: Bad mines (ðŸ’£)\n"
            f"âœ… Green: Safe diamonds (ðŸ’Ž)\n\n"
            f"Contact {ADMIN_USERNAME} for help",
            reply_markup=reply_markup
        )
        await update.message.delete()
        return

    if user_id in channel_members and update.message.text == BOT_PASSWORD:
        verified_users[user_id] = True
        keyboard = [
            [InlineKeyboardButton(f"{i} Mines", callback_data=f'mines_{i}') for i in range(1, 4)],
            [InlineKeyboardButton(f"{i} Mines", callback_data=f'mines_{i}') for i in range(4, 7)],
            [InlineKeyboardButton(f"{i} Mines", callback_data=f'mines_{i}') for i in range(7, 10)],
            [InlineKeyboardButton("10 Mines", callback_data='mines_10')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("âœ… Password correct! Select number of mines:", reply_markup=reply_markup)
        await update.message.delete()
    elif update.message.text == BOT_PASSWORD:
        await update.message.reply_text("Please verify channel membership first!")
        await update.message.delete()


def generate_mines_prediction(num_mines, seed=None, turbo_mode=False):
    import random
    if seed:
        random.seed(hash(seed + ('turbo' if turbo_mode else 'normal')))

    # Define number of good mines based on selection
    mine_map = {
        1: 17, 2: 11, 3: 8, 4: 7, 5: 6,
        6: 5, 7: 4, 8: 3, 9: 3, 10: 2
    }
    good_mines = mine_map.get(num_mines, 2)

    grid = [['ðŸ’£' for _ in range(5)] for _ in range(5)]
    # Place good mines
    good_spots = random.sample([(i, j) for i in range(5) for j in range(5)], good_mines)
    for i, j in good_spots:
        grid[i][j] = 'ðŸ’Ž'
    return grid

def format_prediction(grid):
    return '\n'.join([''.join(row) for row in grid])


def main():
    # Create the bot application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("daily", daily_reward))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


    # Run the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
