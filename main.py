# code wrote : @jokerpython3
import telebot
from telebot.types import InlineKeyboardButton as btn
from telebot.types import InlineKeyboardMarkup as mk
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.account import (
    GetPasswordRequest,
    GetAuthorizationFormRequest,
)
from telethon.errors import (
    PhoneCodeEmptyError,
    PhoneNumberBannedError,
    PhoneNumberInvalidError,
    PhoneNumberFloodError,
    SessionPasswordNeededError,
)
from telethon.functions import (
    payments,
)  # .CheckGiftCodeRequest // .ApplyGiftCodeRequest // .GetStarGiftsRequest // .SendStarsFormRequest // .GetStarsStatusRequest
import asyncio
import os
import json
import threading
from telethon.tl.types import InputPeerUser, InputInvoiceStarGift, InputInvoiceMessage


async def gif(back, m3, session, idd, zp, id):
    try:
        client = TelegramClient(
            StringSession(session),
            api_id=25217515,
            api_hash="1bb27e5be73593e33fc735c1fbe0d855",
        )
        await client.start()

        me = await client.get_me()
        receiver_access_hash = me.access_hash
        receiver_id = me.id
        peer = InputPeerUser(me.id, me.access_hash)
        stars_status = await client(payments.GetStarsStatusRequest(peer=peer))

        stars = stars_status.balance.amount
        gifts_result = await client(payments.GetStarGiftsRequest(hash=0))
        gifts = gifts_result.gifts

        can_buy = False
        message_lines = [f"Your stars: {stars}\n\nAvailable gifts you can buy:\n"]

        for gift in gifts:
            if gift.stars <= stars and not gift.sold_out:
                can_buy = True
                message_lines.append(
                    f"Gift ID: {gift.id}\n"
                    f"Stars Required: {gift.stars}\n"
                    f"Convert Stars: {gift.convert_stars}\n"
                    f"Limited: {gift.limited}\n"
                    f"Sold Out: {gift.sold_out}\n"
                    f"Birthday: {gift.birthday}\n"
                    "-----------------------------"
                )

        if not can_buy:
            text = "No gifts available to buy with your stars."
            bot.edit_message_text(
                chat_id=idd,
                message_id=zp,
                text=f"<strong>{text}</strong>",
                reply_markup=m3,
                parse_mode="html",
            )
        else:
            text = "\n".join(message_lines)
            buy = btn(text="buy", callback_data="buy")
            m_buy = mk().add(buy, back)
            bot.edit_message_text(
                chat_id=idd,
                message_id=zp,
                text=f"<strong>{text}</strong>",
                reply_markup=m_buy,
                parse_mode="html",
            )
            receiver = InputPeerUser(
                user_id=receiver_id, access_hash=receiver_access_hash
            )
            if not os.path.exists("gif.json"):
                with open("gif.json", "w") as f:
                    json.dump({}, f)
            with open("gif.json", "r") as d:
                data = json.load(d)
            data[id] = {
                "session": session,
                "gift_id": gift.id,
                "message": "ksj hilo",
                "receiver": receiver,
                "peer": peer,
            }
        await client.disconnect()
    except Exception as e:
        print(e)
        bot.edit_message_text(
            chat_id=idd,
            message_id=zp,
            text=f"<strong>Bad session, please login a new session.</strong>",
            reply_markup=m3,
            parse_mode="html",
        )


async def buy(id, idd, mes, back, m3):
    with open("data.json", "r") as cv:
        data = json.load(cv)
    gif_id = data[id]["gif_id"]
    session = data[id]["session"]
    receiver = data[id]["receiver"]
    peer = data[id]["peer"]
    try:
        client = TelegramClient(
            StringSession(session),
            api_id=25217515,
            api_hash="1bb27e5be73593e33fc735c1fbe0d855",
        )
        await client.start()

    except:
        bot.edit_message_text(
            chat_id=idd,
            message_id=mes,
            text=f"<strong> exipred session </strong>",
            parse_mode="html",
            reply_markup=m3,
        )
    try:
        payment_form = await client(
            payments.GetPaymentFormRequest(
                invoice=InputInvoiceMessage(peer=peer, msg_id=gif_id)
            )
        )
        result = await client(
            payments.SendStarsFormRequest(
                form_id=payment_form.form_id,
                invoice=InputInvoiceMessage(peer=peer, msg_id=gif_id),
            )
        )
        bot.edit_message_text(
            chat_id=idd,
            message_id=mes,
            text=f"reult : {result.stringify()}\n",
            reply_markup=m3,
        )
        await client.disconnected()
    except:
        bot.edit_message_text(
            chat_id=idd,
            message_id=mes,
            text=f"<strong> error buy gift </strong>",
            parse_mode="html",
            reply_markup=m3,
        )

tok = input("enter token :")
bot = telebot.TeleBot(tok)
print("bot is running now")


@bot.message_handler(commands=["start"])
def start(message):
    b1 = btn(text="login account", callback_data="login")
    b2 = btn(text="developer", url="https://t.me/JokerPython3")
    b3 = btn(text="start search gif ", callback_data="start_search_gif")
    m1 = mk(row_width=1).add(b1, b2, b3)
    text = message.text.split()
    id = str(message.from_user.id)
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({}, f)
    with open("users.json", "r") as s:
        users = json.load(s)
    if id not in users:
        users[id] = {"pointes": 0, "sher": 0}
        try:
            text_sher = text[1]
            if text_sher in users and text_sher != id:
                users[text_sher]["pointes"] += 1
                users[text_sher]["sher"] += 1
            else:
                bot.send_message(
                    message.chat.id,
                    f"""<strong> welcom to serach give bot </strong>""",
                    reply_markup=m1,
                    parse_mode="html",
                )
        except:
            bot.send_message(
                message.chat.id,
                f"""<strong> welcom to serach give bot </strong>""",
                reply_markup=m1,
                parse_mode="html",
            )
    else:
        bot.send_message(
            message.chat.id,
            f"""<strong> welcom to serach give bot </strong>""",
            reply_markup=m1,
            parse_mode="html",
        )
    with open("users.json", "w") as h:
        json.dump(users, h)


@bot.callback_query_handler(func=lambda call: True)
def call(call):
    if call.data == "login":
        back = btn(text="back", callback_data="back")
        b1 = btn(text="Login by session", callback_data="sessionLogin")
        b2 = btn(text="login by phone", callback_data="loginPhone")
        m2 = mk(row_width=1).add(b1, b2, back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="<strong> choice </strong>",
            parse_mode="html",
            reply_markup=m2,
        )
    elif call.data == "loginPhone":
        back = btn(text="back", callback_data="back")
        m6 = mk(row_width=1).add(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="<strong> send phon number with + </strong>",
            parse_mode="html",
            reply_markup=m6,
        )

        @bot.message_handler(func=lambda message: True)
        def login_phone(message):
            phone = message.text
            id = str(message.from_user.id)
            asyncio.run(send_code(phone, message.chat.id, id))

        async def send_code(phone, idd, id):
            client = TelegramClient(
                StringSession(),
                api_id=25217515,
                api_hash="1bb27e5be73593e33fc735c1fbe0d855",
            )
            await client.connect()
            try:
                send = await client.send_code_request(phone)
                hash = send.phone_code_hash
                back = btn(text="back", callback_data="back")
                m8 = mk(row_width=1).add(back)
                bot.send_message(
                    idd,
                    "<strong> done send code please send code now </strong>",
                    reply_markup=m8,
                    parse_mode="html",
                )

                @bot.message_handler(func=lambda message: True)
                def code_text(message):
                    code = message.text.strip()
                    print(code)
                    if not os.path.exists("login.json"):
                        with open("login.json", "w") as ll:
                            json.dump({}, ll)
                    with open("login.json", "r") as f:
                        users = json.load(f)
                    users[id] = {"code": code, "phone": phone, "hash": hash}
                    with open("login.json", "w") as x:
                        json.dump(users, x)
                    print("done save")

                await check_code(id, idd)

            except Exception as e:
                print("3333222")
                print(e)

                back = btn(text="back", callback_data="back")
                m7 = mk(row_width=1).add(back)
                bot.send_message(
                    idd,
                    text="<strong> error send code to number please check number and try agine </strong>",
                    parse_mode="html",
                    reply_markup=m7,
                )

        async def check_code(idd, id):
            print("start check code")
            client = TelegramClient(
                StringSession(),
                api_id=25217515,
                api_hash="1bb27e5be73593e33fc735c1fbe0d855",
            )
            await client.connect()
            try:
                with open("login.json", "r") as f:
                    data = json.load(f)
                phone = data[id]["phone"]
                code = data[id]["code"]
                hash = data[id]["hash"]
                check = await client.sign_in(
                    phone=phone, code=code, phone_code_hash=hash
                )
                back = btn(text="back", callback_data="back")
                b1 = btn("start search gif", callback_data="start_search_gif")
                m9 = mk(row_width=1).add(back, b1)
                bot.send_message(
                    idd,
                    "<strong> done login </strong>",
                    reply_markup=m9,
                    parse_mode="html",
                )
                session = client.session.save()
                client.send_message("me", session)

            except SessionPasswordNeededError:
                m9 = mk(row_width=1).add(back)
                bot.send_message(
                    idd,
                    "<strong> send password account </strong>",
                    reply_markup=m9,
                    parse_mode="html",
                )

                @bot.message_handler(func=lambda message: True)
                def check_password(message):
                    password = message.text

                # asyncio.run(check_password(phone, hash, code, password, idd))

            except PhoneCodeEmptyError:
                m9 = mk(row_width=1).add(back)
                bot.send_message(
                    idd,
                    "<strong> bad code please try agine </strong>",
                    reply_markup=m9,
                    parse_mode="html",
                )
            except Exception as e:
                print(e)

        async def check_password(phone, hash, code, password, idd):
            client = TelegramClient(
                StringSession(),
                api_id=25217515,
                api_hash="1bb27e5be73593e33fc735c1fbe0d855",
            )
            await client.connect()
            try:
                login = client.sign_in(
                    phone=phone, password=password, code=code, phone_code_hash=hash
                )
                back = btn(text="back", callback_data="back")
                b1 = btn("start search gif", callback_data="start_search_gif")
                m9 = mk(row_width=1).add(back, b1)
                bot.send_message(
                    idd,
                    "<strong> done login </strong>",
                    reply_markup=m9,
                    parse_mode="html",
                )
                session = client.session.save()
                client.send_message("me", session)
            except:
                m9 = mk(row_width=1).add(back)
                bot.send_message(
                    idd,
                    "<strong> bad password please checl password and try agine </strong>",
                    reply_markup=m9,
                    parse_mode="html",
                )

    elif call.data == "sessionLogin":
        back = btn(text="back", callback_data="back")
        m3 = mk(row_width=1).add(back)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text="<strong> send a String Session </strong>",
            parse_mode="html",
            reply_markup=m3,
        )

        @bot.message_handler(func=lambda message: True)
        def login_session(message):
            session = message.text
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                client = TelegramClient(
                    StringSession(session),
                    api_id=25217515,
                    api_hash="1bb27e5be73593e33fc735c1fbe0d855",
                    loop=loop,
                )
                back = btn(text="back", callback_data="back")
                b1 = btn("start search gif", callback_data="start_search_gif")
                m4 = mk(row_width=1).add(b1, back)
                bot.send_message(
                    call.message.chat.id,
                    text="<strong> Done Login select your choice </strong>",
                    parse_mode="html",
                    reply_markup=m4,
                )
                id = str(call.message.from_user.id)
                with open("users.json", "r") as f:
                    users = json.load(f)
                users[id] = {"session": session}
                with open("users.json", "w") as x:
                    json.dump(users, x)
                print("hh")

            except:
                back = btn(text="back", callback_data="back")

                m5 = mk(row_width=1).add(back)
                bot.send_message(
                    call.message.chat.id,
                    text="<strong> error login </strong>",
                    parse_mode="html",
                    reply_markup=m5,
                )

    elif call.data == "start_search_gif":
        with open("users.json", "r") as c:
            users = json.load(c)
        id = str(call.message.from_user.id)
        session = users[id]["session"]

        back = btn(text="back", callback_data="back")
        m3 = mk(row_width=1).add(back)
        idd = call.message.chat.id
        zp = call.message.id
        id = str(call.message.from_user.id)

        threading.Thread(
            target=lambda: asyncio.run(gif(back, m3, session, idd, zp, id))
        ).start()
    elif call.data == "buy":
        id = str(call.message.from_user.id)
        idd = call.message.chat.id
        mes = call.message.id
        back = btn(text="back", callback_data="back")
        m3 = mk(row_width=1).add(back)
        threading.Thread(
            target=lambda: asyncio.run(buy(back, m3, session, idd, id))
        ).start()

    elif call.data == "back":
        b1 = btn(text="login account", callback_data="login")
        b2 = btn(text="developer", url="https://t.me/JokerPython3")
        m1 = mk(row_width=1).add(b1, b2)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f"""<strong> welcom to serach give bot </strong>""",
            reply_markup=m1,
            parse_mode="html",
        )


bot.infinity_polling()
