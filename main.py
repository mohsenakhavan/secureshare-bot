import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import uuid
import logging
import shutil
import requests
import asyncio
import time

# Existing logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Existing configuration
TOKEN = 'BOT-TOKEN'
OWNER_IDS = [000000000,000000000]
DISCORD_WEBHOOK_URL = 'DISCORD_WEBHOOK'
REQUIRED_CHANNELS = ['@securexweb','@securexweb']

# Database setup
conn = sqlite3.connect('files.db')
c = conn.cursor()

# Create tables
c.execute('''CREATE TABLE IF NOT EXISTS files
             (unique_id TEXT PRIMARY KEY, file_id TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS file_stats
             (unique_id TEXT PRIMARY KEY, likes INTEGER DEFAULT 0, dislikes INTEGER DEFAULT 0, downloads INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS user_actions
             (user_id INTEGER, file_id TEXT, action TEXT, PRIMARY KEY (user_id, file_id, action))''')
conn.commit()

file_send_count = 0
last_start_times = {}

async def start(update: Update, context):
    global last_start_times
    user_id = update.effective_user.id
    current_time = time.time()

    if user_id in last_start_times and current_time - last_start_times[user_id] < 5:
        await update.message.reply_text("Please wait 5 seconds and try again.")
        return

    last_start_times[user_id] = current_time

    args = context.args

    if args:
        await check_membership(update, context, args[0], send_if_member=True)
    elif user_id in OWNER_IDS:
        await update.message.reply_text("Hello, admin! Send your file to receive a unique link.")

async def check_membership(update: Update, context, file_id, send_if_member=False):
    user_id = update.effective_user.id
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                if send_if_member:
                    await show_channels(update, context, file_id)
                else:
                    await update.callback_query.answer("You haven't joined all required channels. Please join.")
                return
        except Exception as e:
            logger.error(f"Error checking membership: {e}")
            await update.callback_query.answer("Sorry, there was an error checking your membership. Please try again later.")
            return

    if send_if_member:
        await send_file(update, context, file_id)
    else:
        await update.callback_query.message.delete()
        await update.callback_query.answer("Your membership is confirmed!", show_alert=True)
        await send_file(update, context, file_id)

async def show_channels(update: Update, context, file_id):
    keyboard = []
    
    for index, channel in enumerate(REQUIRED_CHANNELS, start=1):
        button_text = f"Join {index}"
        keyboard.append([InlineKeyboardButton(button_text, url=f"https://t.me/{channel[1:]}")])

    keyboard.append([InlineKeyboardButton("Check Membership", callback_data=f"check_{file_id}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Please join the following channels and then click 'Check Membership':",
        reply_markup=reply_markup
    )

async def handle_file(update: Update, context):
    global file_send_count
    user_id = update.effective_user.id
    if user_id not in OWNER_IDS:
        await update.message.reply_text("You are not authorized to upload files.")
        return

    file = update.message.document or update.message.video or update.message.audio or (update.message.photo[-1] if update.message.photo else None)

    if update.message.video:
        file = update.message.video

    if file:
        file_id = file.file_id
        unique_id = str(uuid.uuid4())
        
        c.execute("INSERT INTO files (unique_id, file_id) VALUES (?, ?)", (unique_id, file_id))
        conn.commit()

        link = f"https://t.me/{context.bot.username}?start={unique_id}"
        await update.message.reply_text(f"Your file link: {link}\n\nUsers can click this link to receive the file.")

        file_send_count += 1
        if file_send_count >= 5:
            await backup_database_and_send()
            file_send_count = 0
    else:
        await update.message.reply_text("Please send a file, video, audio, or photo.")

async def backup_database_and_send():
    try:
        shutil.copy('files.db', 'files_backup.db')
        with open('files_backup.db', 'rb') as backup_file:
            requests.post(DISCORD_WEBHOOK_URL, files={'file': backup_file})
        logger.info("Backup sent successfully.")
    except Exception as e:
        logger.error(f"Error in backup and sending to Discord: {e}")

async def send_file(update: Update, context, file_id):
    c.execute("SELECT file_id FROM files WHERE unique_id=?", (file_id,))
    row = c.fetchone()

    if row:
        file_id_to_send = row[0]
        try:
            sent_message = await context.bot.send_document(chat_id=update.effective_chat.id, document=file_id_to_send)
        except Exception as e:
            logger.error(f"Error sending file: {e}")
            try:
                sent_message = await context.bot.send_video(chat_id=update.effective_chat.id, video=file_id_to_send)
            except Exception as e:
                logger.error(f"Error sending video: {e}")
                try:
                    sent_message = await context.bot.send_audio(chat_id=update.effective_chat.id, audio=file_id_to_send)
                except Exception as e:
                    logger.error(f"Error sending audio: {e}")
                    try:
                        sent_message = await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file_id_to_send)
                    except Exception as e:
                        logger.error(f"Error sending photo: {e}")
                        await update.effective_message.reply_text("Sorry, there was a problem sending the file. Please try again later.")
                        return
        
        # Update download count
        c.execute("INSERT OR IGNORE INTO file_stats (unique_id) VALUES (?)", (file_id,))
        c.execute("UPDATE file_stats SET downloads = downloads + 1 WHERE unique_id = ?", (file_id,))
        conn.commit()

        # Fetch current stats
        c.execute("SELECT likes, dislikes, downloads FROM file_stats WHERE unique_id = ?", (file_id,))
        likes, dislikes, downloads = c.fetchone()

        # Create inline keyboard
        keyboard = [
            [
                InlineKeyboardButton(f"👍 {likes}", callback_data=f"like_{file_id}"),
                InlineKeyboardButton(f"👎 {dislikes}", callback_data=f"dislike_{file_id}")
            ],
            [InlineKeyboardButton(f"Downloads: {downloads}", callback_data=f"downloads_{file_id}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send message with buttons and channel ID
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Attention\nSubmitted media will be deleted after [30] seconds. Please save the message in your messenger.\n\n@securexweb",
            reply_markup=reply_markup
        )
        asyncio.create_task(delete_message_after_delay(sent_message, 30))
    else:
        await update.effective_message.reply_text("File not found or invalid link.")

async def delete_message_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()

async def button_callback(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = query.data.split('_')
    action = data[0]
    file_id = data[1]
    user_id = query.from_user.id

    if action in ['like', 'dislike']:
        # Check if user has already performed this action
        c.execute("SELECT * FROM user_actions WHERE user_id = ? AND file_id = ? AND action = ?", (user_id, file_id, action))
        if c.fetchone() is None:
            # User hasn't performed this action before, so update the count
            c.execute(f"UPDATE file_stats SET {action}s = {action}s + 1 WHERE unique_id = ?", (file_id,))
            c.execute("INSERT INTO user_actions (user_id, file_id, action) VALUES (?, ?, ?)", (user_id, file_id, action))
            conn.commit()

            # Fetch updated stats
            c.execute("SELECT likes, dislikes, downloads FROM file_stats WHERE unique_id = ?", (file_id,))
            likes, dislikes, downloads = c.fetchone()

            # Update inline keyboard
            keyboard = [
                [
                    InlineKeyboardButton(f"👍 {likes}", callback_data=f"like_{file_id}"),
                    InlineKeyboardButton(f"👎 {dislikes}", callback_data=f"dislike_{file_id}")
                ],
                [InlineKeyboardButton(f"Downloads: {downloads}", callback_data=f"downloads_{file_id}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_reply_markup(reply_markup=reply_markup)
        else:
            await query.answer("You've already voted for this file.", show_alert=True)
    elif action == 'downloads':
        await query.answer(f"This file has been downloaded {data[2]} times.", show_alert=True)
    elif action == 'check':
        await check_membership(update, context, file_id)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL | filters.VIDEO | filters.AUDIO | filters.PHOTO, handle_file))
    application.add_handler(CallbackQueryHandler(button_callback))

    application.run_polling()

if __name__ == '__main__':
    main()