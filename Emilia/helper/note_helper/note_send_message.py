import html
import re

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Emilia import BOT_USERNAME, pgram
from Emilia.helper.button_gen import button_markdown_parser
from Emilia.helper.note_helper.note_fillings import NoteFillings
from Emilia.helper.note_helper.note_misc_helper import preview_text_replace
from Emilia.mongo.notes_mongo import GetNote
from Emilia.pyro.connection.connection import connection


async def SendNoteMessage(message: Message, note_name: str, from_chat_id: int):
    message.from_user.id
    if await connection(message) is not None:
        from_chat_id = await connection(message)
        message_id = message.migrate_from_chat_id
        content, text, data_type = await GetNote(from_chat_id, note_name)
        chat_id = message.from_user.id
    else:
        # if /privatenotes on
        if from_chat_id is not None:
            message_id = message.id
            chat_id = message.from_user.id
            content, text, data_type = await GetNote(from_chat_id, note_name)
            text = f"**{note_name}:**\n\n" f"{text}"

        else:
            message_id = message.id
            if message.reply_to_message:
                message_id = message.reply_to_message.id
            chat_id = message.chat.id
            content, text, data_type = await GetNote(chat_id, note_name)

    text, buttons = button_markdown_parser(text)
    preview, text = await preview_text_replace(text)

    text = await NoteFillings(message, text)

    text = html.escape(text)

    # Check if string is empty or contain spaces only
    if not text or re.search(r"^\s*$", text):
        text = note_name

    reply_markup = None
    if len(buttons) > 0:
        reply_markup = InlineKeyboardMarkup(buttons)
    elif "{rules}" in text:
        text = text.replace("{rules}", "")
        button = [
            [
                InlineKeyboardButton(
                    text="Rules",
                    url=f"http://t.me/{BOT_USERNAME}?start=rules_{chat_id}",
                )
            ]
        ]
        reply_markup = InlineKeyboardMarkup(button)
    else:
        reply_markup = None

    if data_type == 1:
        await pgram.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
            disable_web_page_preview=preview,
        )

    elif data_type == 2:
        await pgram.send_sticker(
            chat_id=chat_id,
            sticker=content,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    elif data_type == 3:
        await pgram.send_animation(
            chat_id=chat_id,
            animation=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    elif data_type == 4:
        await pgram.send_document(
            chat_id=chat_id,
            document=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    elif data_type == 5:
        await pgram.send_photo(
            chat_id=chat_id,
            photo=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    elif data_type == 6:
        await pgram.send_audio(
            chat_id=chat_id,
            audio=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )
    elif data_type == 7:
        await pgram.send_voice(
            chat_id=chat_id,
            voice=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    elif data_type == 8:
        await pgram.send_video(
            chat_id=chat_id,
            video=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    elif data_type == 9:
        await pgram.send_video_note(
            chat_id=chat_id,
            video_note=content,
            reply_to_message_id=message_id,
            reply_markup=reply_markup,
        )

    return


# Exceptions [400 BUTTON_URL_INVALID]: The button url is invalid (caused
# by "messages.SendMessage")


async def exceNoteMessageSender(message, note_name, from_chat_id=None):
    try:
        await SendNoteMessage(message, note_name, from_chat_id)
    except Exception as e:
        await message.reply(
            (
                "The notedata was incorrect, please update it. The buttons are most likely to be broken. If you are sure you aren't doing anything wrong and this was unexpected - please report it in my support chat.\n"
                f"**Error:** `{e}`"
            ),
            quote=True,
        )
