import logging
import requests


import os

from telegram.ext import Updater, CommandHandler

from genshinstats import GenshinClient, WSError

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',

                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Initialize the Genshin Impact client

client = GenshinClient()

def start(update, context):

    """Send a message when the command /start is issued."""

    context.bot.send_message(chat_id=update.effective_chat.id, text='Hi! I am a Genshin Impact stats bot. Use /stats <player_name> to see a player\'s stats.')

def stats(update, context):

    """Fetch player stats and send them as a message."""

    if not context.args:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter a player name. Usage: /stats <player_name>")

        return

    

    player_name = context.args[0]

    

    try:

        user = client.get_user_stats(player_name)

    except WSError as e:

        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error fetching stats for {player_name}: {e}")

        logger.error(f"Error fetching stats for {player_name}: {e}")

        return

    

    message = f"Stats for {player_name}:\nAdventure Rank: {user.stats.level} ({user.stats.xp_current}/{user.stats.xp_max} XP)\nAchievement Points: {user.stats.achievement_points}\nCharacters:\n"

    

    for char in user.characters:

        message += f"{char.name} ({char.rarity}* {char.element})\nLevel: {char.level_current}\n\n"

    

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def help_command(update, context):

    """Send a message when the command /help is issued."""

    commands = ['/start', '/stats <player_name>']

    help_text = "Here are the available commands:\n"

    for command in commands:

        help_text += f"{command}\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

def main():

    """Start the bot."""

    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

    # Create the Updater and pass it the bot's token.

    updater = Updater(token=TOKEN, use_context=True)

    # Add command handlers

    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CommandHandler('stats', stats))

    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    # Start the bot

    updater.start_polling()

    logger.info("Bot started")

    updater.idle()

if __name__ == '__main__':

    main()

