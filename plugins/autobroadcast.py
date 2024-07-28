import asyncio

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from config import AUTO_GCAST, AUTO_GCAST_MSG, LOGGER_ID
from VIPMUSIC import app
from VIPMUSIC.utils.database import get_served_chats

# Convert AUTO_GCAST to boolean based on "On" or "Off"
AUTO_GCASTS = AUTO_GCAST.strip().lower() == "on"

MESSAGES = f"""**@grandxmasti**"""

caption = f"""{AUTO_GCAST_MSG}""" if AUTO_GCAST_MSG else MESSAGES

TEXT = """**ᴀᴜᴛᴏ ɢᴄᴀsᴛ ɪs ᴇɴᴀʙʟᴇᴅ sᴏ ᴀᴜᴛᴏ ɢᴄᴀsᴛ/ʙʀᴏᴀᴅᴄᴀsᴛ ɪs ᴅᴏɪɴɢ ɪɴ ᴀʟʟ ᴄʜᴀᴛs ᴄᴏɴᴛɪɴᴜᴏᴜsʟʏ.**\n**ɪᴛ ᴄᴀɴ ʙᴇ sᴛᴏᴘᴘᴇᴅ ʙʏ ᴘᴜᴛ ᴠᴀʀɪᴀʙʟᴇ [ᴀᴜᴛᴏ_ɢᴄᴀsᴛ = (Off)]**"""


async def send_text_once():
    try:
        await app.send_message(LOGGER_ID, TEXT)
    except Exception as e:
        pass


async def send_message_to_chats():
    try:
        chats = await get_served_chats()

        for chat_info in chats:
            chat_id = chat_info.get("chat_id")
            if isinstance(chat_id, int):  # Check if chat_id is an integer
                try:
                    await app.send_photo(
                        chat_id,
                        photo=START_IMG_URLS,
                        caption=caption,
                        reply_markup=BUTTONS,
                    )
                    await asyncio.sleep(
                        20
                    )  # Sleep for 20 seconds between sending messages
                except Exception as e:
                    pass  # Do nothing if an error occurs while sending message
    except Exception as e:
        pass  # Do nothing if an error occurs while fetching served chats


async def continuous_broadcast():
    await send_text_once()  # Send TEXT once when bot starts

    while True:
        if AUTO_GCASTS:
            try:
                await send_message_to_chats()
            except Exception as e:
                pass

        # Wait for 100000 seconds before next broadcast
        await asyncio.sleep(100000)


# Start the continuous broadcast loop if AUTO_GCASTS is True
if AUTO_GCASTS:
    asyncio.create_task(continuous_broadcast())
