from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import telebot

tok = input("enter token :")
id = input("enter id")
bot = telebot.TeleBot(tok)
with TelegramClient(
    StringSession(), api_id=25217515, api_hash="1bb27e5be73593e33fc735c1fbe0d855"
) as client:

    session = client.session.save()
    bot.send_message(id, f"<code>{session}</code>", parse_mode="html")
